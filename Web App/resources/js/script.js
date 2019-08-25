/*
 * File: script.js
 * Project: Grid Web App
 * File Created: Wednesday, 21st August 2019 12:51:48 PM
 * Author: nknab
 * Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
 * Version: 1.0
 * Brief: 
 * -----
 * Last Modified: Sunday, 25th August 2019 10:50:28 AM
 * Modified By: nknab
 * -----
 * Copyright ©2019 nknab
 */

const orders_table = document.querySelector("#orders-table");
const depots_list = document.querySelector("#depots-list");

const pp = document.querySelector("#pp");
const db = document.querySelector("#db");

var ipInput = $("#ip").ipInput();

var trackDone = 0;
var orderObjectOne, orderObjectTwo = [];

var MAX_WIDTH = 150;
// Get the modal
var modal = document.getElementById("editModal");

// Get the button that opens the modal
var btnPP = document.getElementById("editButtonPP");
var btnDB = document.getElementById("editButtonDB");

var btnPPTest = document.getElementById("testButtonPP");
var btnDBTest = document.getElementById("testButtonDB");

var stop = document.getElementById("stop");

var cancelBtn = document.getElementById("cancelButton");
var orderBtn = document.getElementById("orderButton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var cancelBtnModal = document.getElementById("modal-btn-cancel");
var saveBtnModal = document.getElementById("modal-btn-save");

var loader = document.getElementById("loader");
var edID = 1;


function drawImg(grid) {
    var image = "img-" + grid;
    var x = document.getElementById(grid);
    var canvax = x.getContext("2d"); //getContext untuk mendeklarasikan dimensi canvas yang kita buat di var x
    var imgElement = document.getElementById(image);
    var imgObj = new Image();
    imgObj.src = imgElement.src;

    var imgW = imgObj.width;
    var imgH = imgObj.height;
    var aspectRatio = imgW / imgH;
    imgW = MAX_WIDTH + 45;
    imgH = MAX_WIDTH / aspectRatio - 45;

    var imgX = (canvax.canvas.width - imgW) / 2;
    var imgY = (canvax.canvas.height - imgH) / 2;

    document.getElementById(grid).style.backgroundImage = "none";
    imgObj.onload = function () {
        //load image on canvas
        canvax.clearRect(0, 0, canvax.canvas.width, canvax.canvas.height); //bersihkan canvas dari gambar sebelumnya
        canvax.drawImage(imgObj, imgX, imgY, imgW, imgH); //place image on canvas in x & y coordinat = 10
    };
}

function saveImage(print_matrix) {
    var canvas = document.createElement("canvas");

    var height = 1920;
    var width = 1920;

    canvas.height = height;
    canvas.width = width;

    var imgObjOne = new Image();
    imgObjOne.src = "resources/images/patterns/pattern-one.png";

    var imgObjTwo = new Image();
    imgObjTwo.src = "resources/images/patterns/pattern-two.png";

    var imgObjThree = new Image();
    imgObjThree.src = "resources/images/patterns/pattern-three.png";

    var imgObjFour = new Image();
    imgObjFour.src = "resources/images/patterns/pattern-four.png";

    var imgObjWhite = new Image();
    imgObjWhite.src = "resources/images/patterns/white.png";

    var context = canvas.getContext("2d");

    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var i = 0;
    var j = 0;
    var n = 0;
    var count = 0;
    for (x of print_matrix) {
        for (y of x) {
            switch (y) {
                case 1:
                    context.drawImage(imgObjOne, i, j, 640, 640);
                    break;
                case 2:
                    context.drawImage(imgObjTwo, i, j, 640, 640);
                    break;
                case 3:
                    context.drawImage(imgObjThree, i, j, 640, 640);
                    break;
                case 4:
                    context.drawImage(imgObjFour, i, j, 640, 640);
                    break;
                default:
                    count++;
                    context.drawImage(imgObjWhite, i, j, 640, 640);
            }
            i += 640;
        }
        i = 0;
        j += 640;
    }
    if (count != 9) {
        var d = new Date();
        n = d.getTime();

        var image = canvas.toDataURL("image/jpg", 1.0);
        var imagedata = image.replace(/^data:image\/(png|jpg);base64,/, "");
        //ajax call to save image inside folder
        var data = {
            imgdata: imagedata,
            filename: n
        };
        runPHPScript(data, "POST", "functions/image.php", true);
    }

    return n;
}

function clear() {
    var grid;
    var x;
    var canvax;
    for (var x = 1; x <= 3; x++) {
        for (var y = 1; y <= 3; y++) {
            (function (x, y) {
                grid = "grid" + x + y;
                x = document.getElementById(grid);
                canvax = x.getContext("2d");
                canvax.clearRect(0, 0, canvax.canvas.width, canvax.canvas.height);

                document.getElementById(grid).style.backgroundImage =
                    "url('resources/images/icons/add.png')";
                document.getElementById(grid).style.backgroundPosition = "center";
                document.getElementById(grid).style.backgroundRepeat = "no-repeat";
                document.getElementById(grid).style.backgroundSize = "35%";
            })(x, y);
        }
    }
    $(".order-input-item").val("");
    $(".select-text").val("0");
}

function runPHPScript(data, request_type, script, sync) {
    var reply;
    $.ajax({
        url: script,
        async: sync,
        data: data,
        type: request_type,
        success: function (response) {
            reply = response;
        }
    });
    return reply;
}

function getIP(id) {
    var success = true;
    const inputs = document.querySelectorAll(".ip-input-item");

    var ip_address = "";
    var count = 0;
    for (const input of inputs) {
        if (count == 3) {
            ip_address += input.value;
        } else {
            ip_address += input.value + ".";
        }
        count++;
    }

    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip_address)) {
        data = 'x=' + JSON.stringify({
            id: id,
            ip_address: ip_address
        });
        runPHPScript(data, "POST", "controller/sectors.php", true);
    } else {
        success = false;
    }
    return success;
}

function loadOrdersTable() {
    const request = new XMLHttpRequest();

    request.open("GET", "controller/orders.php?orders=1", true);

    request.onload = () => {
        try {
            const data = JSON.parse(request.responseText);
            populateOrdersTable(data);
        } catch (e) {
            console.warn("Can not Load Orders");
        }
    };
    request.send();
}

function populateDepots() {
    request = "depots=1";
    const data = runPHPScript(request, "GET", "controller/orders.php", false);

    while (depots_list.firstChild) {
        depots_list.removeChild(depots_list.firstChild);
    }

    var html = '<option value="0" disabled selected></option>';

    for (var i = 0; i < data.length; i++) {
        html +=
            '<option value="' +
            data[i].id +
            '">' +
            data[i].name +
            "</option>";
    }

    document.getElementById("depots-list").innerHTML += html;
}



function populateOrdersTable(data) {
    for (var i = data.length - 1; i >= 0; i--) {
        orderObjectTwo.unshift(data[i].order_status);
    }

    var reload = done();

    if (reload == true || trackDone == 1) {
        if (trackDone != 2) {
            trackDone++;
        }
        while (orders_table.firstChild) {
            orders_table.removeChild(orders_table.firstChild);
        }

        var html = "";

        var lastprogress = true;
        var orderName = "Order Name"

        for (var i = 0; i < data.length; i++) {
            if (data[i].order_status != 4 && lastprogress == true) {
                lastprogress = false;
                orderName = data[i].name
                if (data[i].order_status == 1) {
                    document.getElementById("bar1").style.borderColor = "#707070";
                    document.getElementById("bar1").style.backgroundColor = "white";
                    document.getElementById("bar1").style.border = "1.5px solid #707070";

                    document.querySelector("#circle-production > div").style.borderColor =
                        "#707070";
                    document.querySelector("#circle-production > p").style.color =
                        "#707070";
                    document.querySelector("#circle-production > div > img").src =
                        "resources/images/icons/fabric-gray.png";

                    document.getElementById("bar2").style.borderColor = "#707070";
                    document.getElementById("bar2").style.backgroundColor = "white";
                    document.getElementById("bar2").style.border = "1.5px solid #707070";

                    document.querySelector("#circle-delivery > div").style.borderColor =
                        "#707070";
                    document.querySelector("#circle-delivery > p").style.color = "#707070";
                    document.querySelector("#circle-delivery > div > img").src =
                        "resources/images/icons/delivery-truck-gray.png";

                    document.querySelector("#circle-done > div").style.borderColor =
                        "#707070";
                    document.querySelector("#circle-done > p").style.color = "#707070";
                    document.querySelector("#circle-done > div > img").src =
                        "resources/images/icons/checked-gray.png";
                } else if (data[i].order_status == 2) {
                    document.getElementById("bar1").style.border = "1.5px solid #707070";
                    document.getElementById("bar1").style.borderLeft = "40px solid #6AC25A";
                    document.getElementById("bar1").style.backgroundColor = "white";

                    document.querySelector("#circle-production > div").style.borderColor =
                        "#6AC25A";
                    document.querySelector("#circle-production > p").style.color =
                        "#6AC25A";
                    document.querySelector("#circle-production > div > img").src =
                        "resources/images/icons/fabric.png";

                    document.getElementById("bar2").style.borderColor = "#707070";
                    document.getElementById("bar2").style.backgroundColor = "white";
                    document.getElementById("bar2").style.border = "1.5px solid #707070";

                    document.querySelector("#circle-delivery > div").style.borderColor =
                        "#707070";
                    document.querySelector("#circle-delivery > p").style.color = "#707070";
                    document.querySelector("#circle-delivery > div > img").src =
                        "resources/images/icons/delivery-truck-gray.png";

                    document.querySelector("#circle-done > div").style.borderColor =
                        "#707070";
                    document.querySelector("#circle-done > p").style.color = "#707070";
                    document.querySelector("#circle-done > div > img").src =
                        "resources/images/icons/checked-gray.png";
                } else if (data[i].order_status == 3) {
                    document.getElementById("bar1").style.borderColor = "#6AC25A";
                    document.getElementById("bar1").style.backgroundColor = "#6AC25A";
                    document.querySelector("#circle-production > div").style.borderColor =
                        "#6AC25A";
                    document.querySelector("#circle-production > p").style.color =
                        "#6AC25A";
                    document.querySelector("#circle-production > div > img").src =
                        "resources/images/icons/fabric.png";

                    document.getElementById("bar2").style.border = "1.5px solid #707070";
                    document.getElementById("bar2").style.borderLeft = "40px solid #6AC25A";
                    document.getElementById("bar2").style.backgroundColor = "white";

                    // document.getElementById('bar2').style.borderColor = "#707070";

                    document.querySelector("#circle-delivery > div").style.borderColor =
                        "#6AC25A";
                    document.querySelector("#circle-delivery > p").style.color = "#6AC25A";
                    document.querySelector("#circle-delivery > div > img").src =
                        "resources/images/icons/delivery-truck.png";

                    document.querySelector("#circle-done > div").style.borderColor =
                        "#707070";
                    document.querySelector("#circle-done > p").style.color = "#707070";
                    document.querySelector("#circle-done > div > img").src =
                        "resources/images/icons/checked-gray.png";
                } else if (data[i].order_status == 4) {
                    document.getElementById("bar1").style.borderColor = "#6AC25A";
                    document.getElementById("bar1").style.backgroundColor = "#6AC25A";
                    document.querySelector("#circle-production > div").style.borderColor =
                        "#6AC25A";
                    document.querySelector("#circle-production > p").style.color =
                        "#6AC25A";
                    document.querySelector("#circle-production > div > img").src =
                        "resources/images/icons/fabric.png";

                    document.getElementById("bar2").style.borderColor = "#6AC25A";
                    document.getElementById("bar2").style.backgroundColor = "#6AC25A";
                    document.querySelector("#circle-delivery > div").style.borderColor =
                        "#6AC25A";
                    document.querySelector("#circle-delivery > p").style.color = "#6AC25A";
                    document.querySelector("#circle-delivery > div > img").src =
                        "resources/images/icons/delivery-truck.png";

                    document.querySelector("#circle-done > div").style.borderColor =
                        "#6AC25A";
                    document.querySelector("#circle-done > p").style.color = "#6AC25A";
                    document.querySelector("#circle-done > div > img").src =
                        "resources/images/icons/checked.png";
                }
            }
        }
        for (var i = data.length - 1; i >= 0; i--) {

            if (lastprogress == true) {
                orderName = data[data.length - 1].name;

                document.getElementById("bar1").style.borderColor = "#6AC25A";
                document.getElementById("bar1").style.backgroundColor = "#6AC25A";
                document.querySelector("#circle-production > div").style.borderColor =
                    "#6AC25A";
                document.querySelector("#circle-production > p").style.color = "#6AC25A";
                document.querySelector("#circle-production > div > img").src =
                    "resources/images/icons/fabric.png";

                document.getElementById("bar2").style.borderColor = "#6AC25A";
                document.getElementById("bar2").style.backgroundColor = "#6AC25A";
                document.querySelector("#circle-delivery > div").style.borderColor =
                    "#6AC25A";
                document.querySelector("#circle-delivery > p").style.color = "#6AC25A";
                document.querySelector("#circle-delivery > div > img").src =
                    "resources/images/icons/delivery-truck.png";

                document.querySelector("#circle-done > div").style.borderColor =
                    "#6AC25A";
                document.querySelector("#circle-done > p").style.color = "#6AC25A";
                document.querySelector("#circle-done > div > img").src =
                    "resources/images/icons/checked.png";
            }

            if (data[i].order_status == 1) {
                data[i].order_status = ' style = "color:#c0c0c0"/>In Queue';
            } else if (data[i].order_status == 2) {
                data[i].order_status = ' style = "color:#F50000"/>Production';
            } else if (data[i].order_status == 3) {
                data[i].order_status = ' style = "color:#F4A01D"/>In Delivery';
            } else if (data[i].order_status == 4) {
                data[i].order_status = ' style = "color:#6AC25A"/>Done';
            }

            html += '<tr class="rowLine">';
            html +=
                '<td><img src="resources/images/prints/' + data[i].print + '.jpg"></td>';
            html +=
                "<td><h3>" +
                data[i].name +
                '</h3><table class="subTable"><tr><td id="columnOne"><h4>Quantity: <strong>' +
                data[i].quantity +
                '</strong> yards</h4></td><td id="columnTwo"><h4>Depot: <strong>' +
                data[i].depot +
                '</strong></h4></td></tr></table><table class="subTable"><tr><td id="idColumn"><h4>Order ID: <strong>' +
                pad_with_zeroes(data[i].id, 4) +
                '</strong></h4></td><td id="statColumn"><h4 id="statusH4">Status: <strong id="status>"' +
                data[i].order_status +
                '</strong></h4></td></tr></table>'
            html += "</td></tr>";

            document.getElementById("orderName").innerHTML = orderName


        }

        document.getElementById("orders-table").innerHTML += html;

        if (data.length <= 0) {
            document.getElementById("orderName").innerHTML = "Order Name";
            document.getElementById("bar1").style.borderColor = "#707070";
            document.getElementById("bar1").style.backgroundColor = "white";
            document.getElementById("bar1").style.border = "1.5px solid #707070";

            document.querySelector("#circle-production > div").style.borderColor =
                "#707070";
            document.querySelector("#circle-production > p").style.color =
                "#707070";
            document.querySelector("#circle-production > div > img").src =
                "resources/images/icons/fabric-gray.png";

            document.getElementById("bar2").style.borderColor = "#707070";
            document.getElementById("bar2").style.backgroundColor = "white";
            document.getElementById("bar2").style.border = "1.5px solid #707070";

            document.querySelector("#circle-delivery > div").style.borderColor =
                "#707070";
            document.querySelector("#circle-delivery > p").style.color = "#707070";
            document.querySelector("#circle-delivery > div > img").src =
                "resources/images/icons/delivery-truck-gray.png";

            document.querySelector("#circle-done > div").style.borderColor =
                "#707070";
            document.querySelector("#circle-done > p").style.color = "#707070";
            document.querySelector("#circle-done > div > img").src =
                "resources/images/icons/checked-gray.png";
        }
    }

}

function arr_diff(a1, a2) {
    var diff = [];
    var done = []

    for (var i = 0; i < a2.length; i++) {
        if (a1[i] != a2[i]) {
            diff.push(i + 1);
            if (a2[i] == 4) {
                done.push(i + 1);
            }
        }
    }
    return [diff, done];
}

function done() {
    var reload = false;
    var orders = "";
    if (trackDone == 0) {
        orderObjectOne = orderObjectTwo;
        orderObjectTwo = []
        trackDone++;
    } else {
        var diff = arr_diff(orderObjectOne, orderObjectTwo)
        if (diff[0].length > 0) {
            reload = true;
        }
        if (diff[1].length == 1) {
            swal(
                "Order " + pad_with_zeroes(diff[1][0], 4),
                "Your Order Is Done!",
                "success"
            );
        } else if (diff[1].length > 1) {
            for (var i = 0; i < diff[1].length; i++) {
                if (i == diff[1].length - 2) {
                    orders += pad_with_zeroes(diff[1][i], 4) + ", ";
                } else {
                    orders += pad_with_zeroes(diff[1][i], 4);
                }
            }
            swal(
                "Orders Done ",
                "Order Numbers " + orders + " Are Ready.",
                "success"
            );
        }
        orderObjectOne = [];
        orderObjectOne = orderObjectTwo;
        orderObjectTwo = []
    }
    return reload;
}

function pad_with_zeroes(number, length) {
    var my_string = "" + number;
    while (my_string.length < length) {
        my_string = "0" + my_string;
    }

    return my_string;
}

function populateOrdersSectors() {
    request = "";
    const data = runPHPScript(request, "GET", "controller/sectors.php", false);

    while (pp.firstChild) {
        pp.removeChild(pp.firstChild);
        db.removeChild(db.firstChild);
    }

    var html = "";
    html += "<h3>" + data[0].name + "</h3>";
    html += "<h4>" + data[0].ip_address + "</h4>";
    document.getElementById("pp").innerHTML += html;

    html = "";
    html += "<h3>" + data[1].name + "</h3>";
    html += "<h4>" + data[1].ip_address + "</h4>";
    document.getElementById("db").innerHTML += html;
}

// When the user clicks the button, open the modal
btnPP.onclick = function () {
    edID = 1;
    document.getElementById("editModalHeader").innerHTML = "Production Plant";
    modal.style.display = "block";
};

btnDB.onclick = function () {
    edID = 2;
    document.getElementById("editModalHeader").innerHTML = "Delivery Bot";
    modal.style.display = "block";
};

cancelBtn.onclick = function () {
    swal({
        title: "Are you sure?",
        text: "Once Cancelled, you will not be able to recover this Order!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
        buttons: ["Do Not Cancel", "Yes, Cancel Order"]

    }).then(willDelete => {
        if (willDelete) {
            swal("Poof! Order has been Cancelled", {
                icon: "success"
            });
            clear();
        } else {
            swal("Your Order Awaits");
        }
    })
};

btnPPTest.onclick = function () {
    var ip = document.getElementById("pp").getElementsByTagName("h4")[0]
        .innerHTML;
    var data =
        "test=" +
        JSON.stringify({
            server: ip
        });
    runPHPScript(data, "GET", "functions/mqtt.php", true);
    swal("Production Plant Test", "Test Command Has Been Issued", "info");
};

btnDBTest.onclick = function () {
    var ip = document.getElementById("db").getElementsByTagName("h4")[0]
        .innerHTML;
    var data =
        "test=" +
        JSON.stringify({
            server: ip
        });
    runPHPScript(data, "GET", "functions/mqtt.php", true);
    swal("Delivery Bot Test", "Test Command Has Been Issued", "info");
};

stop.onclick = function () {
    var pp = document.getElementById("pp").getElementsByTagName("h4")[0]
        .innerHTML;
    var db = document.getElementById("db").getElementsByTagName("h4")[0]
        .innerHTML;

    var data =
        "stop=" +
        JSON.stringify({
            production: pp,
            delivery: db
        });
    runPHPScript(data, "GET", "functions/mqtt.php", true);
    swal(
        "Emergency Stop!",
        "Emergency Stop Command Has Been Issued!",
        "success"
    );
};

saveBtnModal.onclick = function () {
    var success = getIP(edID);
    var message = "";

    if (success == true) {
        if (edID == 1) {
            message = "Production Plant's IP Address Has Been Changed";
        } else if (edID == 2) {
            message = "Delivery Bot's IP Address Has Been Changed";
        }

        populateOrdersSectors();
        $(".ip-input-item").val("");
        modal.style.display = "none";
        swal("Saved!", message, "success");
    } else {
        swal("Invalid IP Address", "Kindly Enter A Valid IP Address", "error");
    }
};

orderBtn.onclick = function () {
    var printMatrix = [];
    var print_mat = "";
    var countPrintImage = 9;
    var name = document.querySelectorAll(".order-input-item")[0].value;
    var quantity = document.querySelectorAll(".order-input-item")[1].value;

    var dep = document.getElementById("depots-list");
    var depot = dep.options[dep.selectedIndex].value;

    var server = document.getElementById("pp").getElementsByTagName("h4")[0]
        .innerHTML;
    var delivery_bot = document.getElementById("db").getElementsByTagName("h4")[0]
        .innerHTML;

    for (var x = 1; x <= 3; x++) {
        var temp = [];
        for (var y = 1; y <= 3; y++) {
            (function (x, y) {
                grid = "img-grid" + x + y;
                img = document.getElementById(grid).src;
                var tempArr = img.split("/");
                var index = tempArr.slice(-1)[0];
                if (index == "pattern-one.png") {
                    temp.push(1);
                } else if (index == "pattern-two.png") {
                    temp.push(2);
                } else if (index == "pattern-three.png") {
                    temp.push(3);
                } else if (index == "pattern-four.png") {
                    temp.push(4);
                } else {
                    countPrintImage++;
                    temp.push(0);
                }
                if (x == 3 && y == 3) {
                    print_mat += temp[y - 1];
                } else {
                    print_mat += temp[y - 1] + ",";
                }
            })(x, y);
        }
        printMatrix.push(temp);
    }

    if (quantity > 0 && depot > 0 && countPrintImage < 18 && name != "") {
        loader.style.display = "block";
        var success = true;
        setTimeout(function () {
            printImage = saveImage(printMatrix);

            if (printImage != 0) {
                var orderData =
                    "order=" +
                    JSON.stringify({
                        name: name,
                        quantity: Number(quantity),
                        depot: Number(depot),
                        order_status: 1,
                        print: printImage,
                        print_matrix: print_mat
                    });
                var orderID = runPHPScript(
                    orderData,
                    "POST",
                    "controller/orders.php",
                    false
                );
                if (orderID != 0) {
                    var mqttData =
                        "order=" +
                        JSON.stringify({
                            server: server,
                            orderID: orderID,
                            quantity: quantity,
                            depot: depot,
                            print_matrix: printMatrix,
                            // delivery_bot: delivery_bot
                        });
                    runPHPScript(mqttData, "GET", "functions/mqtt.php", true);
                } else {
                    success = false;
                }
            } else {
                success = false;
            }

            if (success) {
                clear();
                loader.style.display = "none";
                swal("Sent!", "Your order has been sent for production!", "success");
            } else {
                loader.style.display = "none";
                swal(
                    "Oops!",
                    "Your order could not be sent for production. Try Again!",
                    "error"
                );
            }
        }, 4000);
    } else if (countPrintImage < 18 && name != "" && quantity > 0 && depot == 0) {
        swal("Depot", "Kindly Provide Depot!", "warning");
    } else if (countPrintImage < 18 && name != "" && quantity <= 0 && depot > 0) {
        swal("Quantity", "Kindly Provide Quantity!", "warning");
    } else if (countPrintImage < 18 && name != "" && quantity <= 0 && depot == 0) {
        swal("Quantity & Depot", "Kindly Provide Quantity and Depot!", "warning");
    } else if (countPrintImage < 18 && name == "" && quantity > 0 && depot > 0) {
        swal("Design Name", "Kindly Provide Design Name!", "warning");
    } else if (countPrintImage < 18 && name == "" && quantity > 0 && depot == 0) {
        swal("Design Name & Depot", "Kindly Provide Design Name and Depot!", "warning");
    } else if (countPrintImage < 18 && name == "" && quantity <= 0 && depot > 0) {
        swal("Design Name & Quantity", "Kindly Provide Design Name and Quantity!", "warning");
    } else if (countPrintImage < 18 && name == "" && quantity <= 0 && depot == 0) {
        swal("Design Name, Quantity & Depot", "Kindly Provide Design Name, Quantity and Depot!", "warning");
    } else if (countPrintImage == 18 && name != "" && quantity > 0 && depot > 0) {
        swal("Print Style", "Kindly Provide Print Style!", "warning");
    } else if (countPrintImage == 18 && name != "" && quantity > 0 && depot == 0) {
        swal("Print Style & Depot", "Kindly Provide Print Style and Depot!", "warning");
    } else if (countPrintImage == 18 && name != "" && quantity <= 0 && depot > 0) {
        swal("Print Style & Quantity", "Kindly Provide Print Style and Quantity!", "warning");
    } else if (countPrintImage == 18 && name != "" && quantity <= 0 && depot == 0) {
        swal("Print Style, Quantity & Depot", "Kindly Provide Print Style, Quantity and Depot!", "warning");
    } else if (countPrintImage == 18 && name == "" && quantity > 0 && depot > 0) {
        swal("Print Style & Design Name", "Kindly Provide Print Style and Design Name!", "warning");
    } else if (countPrintImage == 18 && name == "" && quantity > 0 && depot == 0) {
        swal("Print Style, Design Name & Depot", "Kindly Provide Print Style, Design Name and Depot!", "warning");
    } else if (countPrintImage == 18 && name == "" && quantity <= 0 && depot > 0) {
        swal("Print Style, Design Name & Quantity", "Kindly Provide Print Style, Design Name and Quantity!", "warning");
    } else {
        swal(
            "No Specifications",
            "Kindly Provide Print Style, Design Name, Quantity and Depot!",
            "warning"
        );
    }
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    $(".ip-input-item").val("");
    modal.style.display = "none";
};

cancelBtnModal.onclick = function () {
    $(".ip-input-item").val("");
    modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        $(".ip-input-item").val("");
        modal.style.display = "none";
    }
};

document.addEventListener("DOMContentLoaded", () => {
    loadOrdersTable();
    populateOrdersSectors();
    populateDepots();
    clear();
});

setInterval("loadOrdersTable();", 1000);

$(document).ready(function () {
    $(".stampsContainer div").draggable({
        containment: "document",
        opacity: 1,
        revert: false,
        helper: "clone",
        start: function () {
            $(".infoDrag").text("Start Drag");
        },
        drag: function () {
            $(".infoDrag").text("on Dragging");
        },
        stop: function () {
            $(".infoDrag").text("Stop Dragging");
        }
    });

    for (var x = 1; x <= 3; x++) {
        for (var y = 1; y <= 3; y++) {
            (function (x, y) {
                var grid = "grid" + x + y;
                var id = "#" + grid;
                $(id).droppable({
                    hoverClass: "borda",
                    tolerance: "pointer",
                    drop: function (ev, ui) {
                        var droppedItem = $(ui.draggable).clone();
                        var canvasImg = $(this).find("img");
                        var newSrc = droppedItem.find("img").attr("src");
                        canvasImg.attr("src", newSrc);
                        drawImg(grid);
                    }
                });

                $(id).dblclick(function () {
                    $(id).draggable();
                });

                document.getElementById(grid).style.backgroundImage =
                    "url('resources/images/icons/add.png')";
                document.getElementById(grid).style.backgroundPosition = "center";
                document.getElementById(grid).style.backgroundRepeat = "no-repeat";
                document.getElementById(grid).style.backgroundSize = "35%";
            })(x, y);
        }
    }
});