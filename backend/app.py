from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from database.database import db
from flask import request, redirect, url_for
from models.customer import Customer
import csv
import io
from datetime import datetime
from ai.preprocessing import create_customer_features
from ai.train_model import train_purchase_model
from routes.notification import notification_bp

# Import all models
from models.admin import Admin
from models.customer import Customer
from models.product import Product
from models.notification import Notification
from models.prediction import Prediction
from models.purchase_history import PurchaseHistory
from ai.train_model import create_training_data

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
app.config.from_object(Config)
app.register_blueprint(notification_bp)

db.init_app(app)

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/customers")
def customers():

    customers = Customer.query.all()

    return render_template(
        "customers.html",
        customers=customers
    )


@app.route("/add_customer", methods=["POST"])
def add_customer():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    city = request.form.get("city", "").strip()
    age = request.form.get("age", "").strip()
    preferred_category = request.form.get("preferred_category", "").strip()

    # Check whether email already exists
    existing_customer = Customer.query.filter_by(email=email).first()

    if existing_customer:
        return redirect(
            url_for("customers", error="A customer with this email already exists.")
        )

    customer = Customer(
        name=name,
        email=email,
        phone=phone,
        city=city,
        age=age if age else None,
        preferred_category=preferred_category
    )

    db.session.add(customer)
    db.session.commit()

    return redirect(url_for("customers"))




@app.route("/bulk_import_customers", methods=["POST"])
def bulk_import_customers():

    file = request.files.get("csv_file")

    if not file or file.filename == "":
        return redirect(
            url_for(
                "customers",
                error="Please select a CSV file."
            )
        )

    if not file.filename.lower().endswith(".csv"):
        return redirect(
            url_for(
                "customers",
                error="Please upload a CSV file."
            )
        )

    try:

        # Read CSV file
        stream = io.StringIO(
            file.stream.read().decode("utf-8-sig"),
            newline=None
        )

        reader = csv.DictReader(stream)

        required_columns = {
            "name",
            "email",
            "phone",
            "city",
            "preferred_category"
        }

        # Check CSV columns
        if not reader.fieldnames:

            return redirect(
                url_for(
                    "customers",
                    error="The CSV file is empty."
                )
            )

        csv_columns = {
            column.strip()
            for column in reader.fieldnames
        }

        if not required_columns.issubset(csv_columns):

            missing_columns = required_columns - csv_columns

            return redirect(
                url_for(
                    "customers",
                    error="Missing columns: "
                    + ", ".join(missing_columns)
                )
            )

        added = 0
        skipped = 0

        for row in reader:

            name = row.get("name", "").strip()
            email = row.get("email", "").strip()
            phone = row.get("phone", "").strip()
            city = row.get("city", "").strip()
            preferred_category = row.get(
                "preferred_category", ""
            ).strip()

            # Skip empty rows
            if not name or not email:
                skipped += 1
                continue

            # Check duplicate email
            existing_customer = Customer.query.filter_by(
                email=email
            ).first()

            if existing_customer:
                skipped += 1
                continue

            customer = Customer(
                name=name,
                email=email,
                phone=phone,
                city=city,
                preferred_category=preferred_category
            )

            db.session.add(customer)

            added += 1

        db.session.commit()

        return redirect(
            url_for(
                "customers",
                success=f"{added} customers imported successfully. "
                        f"{skipped} records skipped."
            )
        )

    except Exception as e:

        db.session.rollback()

        return redirect(
            url_for(
                "customers",
                error=f"Import failed: {str(e)}"
            )
        )



@app.route("/bulk_import_purchases", methods=["POST"])
def bulk_import_purchases():

    file = request.files.get("purchase_csv_file")

    if not file or file.filename == "":
        return redirect(
            url_for(
                "customers",
                error="Please select a purchase CSV file."
            )
        )

    if not file.filename.lower().endswith(".csv"):
        return redirect(
            url_for(
                "customers",
                error="Please upload a CSV file."
            )
        )

    try:

        stream = io.StringIO(
            file.stream.read().decode("utf-8-sig"),
            newline=""
        )

        reader = csv.DictReader(stream)

        required_columns = {
            "customer_id",
            "product_name",
            "category",
            "purchase_date",
            "quantity",
            "amount"
        }

        if not reader.fieldnames:
            return redirect(
                url_for(
                    "customers",
                    error="CSV file is empty."
                )
            )

        csv_columns = {
            column.strip()
            for column in reader.fieldnames
        }

        missing_columns = (
            required_columns - csv_columns
        )

        if missing_columns:

            return redirect(
                url_for(
                    "customers",
                    error=(
                        "Missing columns: "
                        + ", ".join(missing_columns)
                    )
                )
            )

        added = 0
        skipped = 0

        for row in reader:

            try:

                customer_id = int(
                    row["customer_id"].strip()
                )

                product_name = row[
                    "product_name"
                ].strip()

                category = row[
                    "category"
                ].strip()

                purchase_date = datetime.strptime(
                    row["purchase_date"].strip(),
                    "%Y-%m-%d"
                ).date()

                quantity = int(
                    row["quantity"].strip()
                )

                amount = float(
                    row["amount"].strip()
                )

                # Validate values

                if not product_name:
                    skipped += 1
                    continue

                if not category:
                    skipped += 1
                    continue

                if quantity <= 0:
                    skipped += 1
                    continue

                if amount < 0:
                    skipped += 1
                    continue

                # Check customer

                customer = Customer.query.get(
                    customer_id
                )

                if customer is None:
                    skipped += 1
                    continue

                # Create purchase

                purchase = PurchaseHistory(

                    customer_id=customer_id,

                    product_name=product_name,

                    category=category,

                    purchase_date=purchase_date,

                    quantity=quantity,

                    amount=amount
                )

                db.session.add(purchase)

                added += 1

            except (ValueError, TypeError):

                skipped += 1

        db.session.commit()

        return redirect(
            url_for(
                "customers",
                success=(
                    f"{added} purchase records "
                    f"imported successfully. "
                    f"{skipped} records skipped."
                )
            )
        )

    except Exception as e:

        db.session.rollback()

        return redirect(
            url_for(
                "customers",
                error=f"Import failed: {str(e)}"
            )
        )


@app.route("/delete_customer/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):

    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    return redirect(url_for("customers"))


@app.route("/edit_customer/<int:customer_id>", methods=["POST"])
def edit_customer(customer_id):

    customer = Customer.query.get_or_404(customer_id)

    customer.name = request.form["name"]
    customer.email = request.form["email"]
    customer.phone = request.form.get("phone")
    customer.city = request.form.get("city")
    customer.age = request.form.get("age")
    customer.preferred_category = request.form.get("preferred_category")

    db.session.commit()

    return redirect(url_for("customers"))



@app.route("/purchase_history")
def purchase_history():

    purchases = (
        PurchaseHistory.query
        .order_by(PurchaseHistory.purchase_date.desc())
        .all()
    )

    return render_template(
        "purchase_history.html",
        purchases=purchases
    )


@app.route("/test_ai_features")
def test_ai_features():

    features = create_customer_features()

    return features.to_html(
        index=False,
        classes="table table-bordered"
    )


@app.route("/test_training_data")
def test_training_data():

    data = create_training_data()

    return data.to_html(
        index=False,
        classes="table table-bordered"
    )




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    app.run(debug=True)