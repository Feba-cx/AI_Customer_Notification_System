const sales=document.getElementById("salesChart");

new Chart(sales,{

type:"line",

data:{

labels:["Jan","Feb","Mar","Apr","May","Jun"],

datasets:[{

label:"Sales",

data:[120,180,160,240,300,380],

borderWidth:3,

tension:.4

}]

}

});

const notify=document.getElementById("notificationChart");

new Chart(notify,{

type:"doughnut",

data:{

labels:["Email","SMS","WhatsApp"],

datasets:[{

data:[52,23,25]

}]

}

});