let passengerChart = null;
let queueChart = null;
let gateChart = null;

function updateClock() {

    const now = new Date();

    document.getElementById("clock").innerHTML =
        now.toLocaleTimeString();

}

async function loadDashboard() {

    const response = await fetch("/api/dashboard/");
    const data = await response.json();

    // KPI Cards

    document.getElementById("passengerCount").innerHTML =
        data.passengers;

    document.getElementById("flowStatus").innerHTML =
        data.flow;

    document.getElementById("queueCount").innerHTML =
        data.queue;

    document.getElementById("gateCount").innerHTML =
        data.gate;

    document.getElementById("temperature").innerHTML =
        data.temperature + "°C";

    document.getElementById("alertStatus").innerHTML =
        data.alert;

    // Recent Activity Table

    document.getElementById("tblPassenger").innerHTML =
        data.passengers;

    document.getElementById("tblQueue").innerHTML =
        data.queue;

    document.getElementById("tblGate").innerHTML =
        data.gate;

    document.getElementById("tblTemp").innerHTML =
        data.temperature + "°C";

    document.getElementById("tblAlert").innerHTML =
        data.alert;

    // Passenger History

    const labels = data.history.map(item => item.time);

    const passengerValues =
        data.history.map(item => item.count);

    // Queue Demo History
    // Replace later with actual queue history from API

    const queueValues = passengerValues.map(v =>
        Math.max(0, Math.round(v * 0.5)));

    // Passenger Chart

    if (!passengerChart) {

        passengerChart = new Chart(

            document
                .getElementById("passengerChart")
                .getContext("2d"),

            {

                type: "line",

                data: {

                    labels: labels,

                    datasets: [

                        {

                            label: "Passengers",

                            data: passengerValues,

                            borderWidth: 3,

                            fill: true,

                            tension: 0.4

                        }

                    ]

                },

                options: {

                    responsive: true,

                    animation: false,

                    plugins: {

                        legend: {

                            display: false

                        }

                    },

                    scales: {

                        y: {

                            beginAtZero: true

                        }

                    }

                }

            }

        );

    }

    else {

        passengerChart.data.labels = labels;

        passengerChart.data.datasets[0].data =
            passengerValues;

        passengerChart.update();

    }

    // Queue Chart

    if (!queueChart) {

        queueChart = new Chart(

            document
                .getElementById("queueChart")
                .getContext("2d"),

            {

                type: "bar",

                data: {

                    labels: labels,

                    datasets: [

                        {

                            label: "Queue",

                            data: queueValues,

                            borderWidth: 1

                        }

                    ]

                },

                options: {

                    responsive: true,

                    animation: false,

                    plugins: {

                        legend: {

                            display: false

                        }

                    },

                    scales: {

                        y: {

                            beginAtZero: true

                        }

                    }

                }

            }

        );

    }

    else {

        queueChart.data.labels = labels;

        queueChart.data.datasets[0].data =
            queueValues;

        queueChart.update();

    }

    // Gate Chart

    if (!gateChart) {

        gateChart = new Chart(

            document
                .getElementById("gateChart")
                .getContext("2d"),

            {

                type: "doughnut",

                data: {

                    labels: [

                        "Occupied",

                        "Available"

                    ],

                    datasets: [

                        {

                            data: [

                                data.gate,

                                Math.max(0, 100 - data.gate)

                            ]

                        }

                    ]

                },

                options: {

                    responsive: true,

                    animation: false

                }

            }

        );

    }

    else {

        gateChart.data.datasets[0].data = [

            data.gate,

            Math.max(0, 100 - data.gate)

        ];

        gateChart.update();

    }

}

updateClock();
loadDashboard();

setInterval(updateClock,1000);
setInterval(loadDashboard,2000);