<!-- 
 * File: index.php
 * Project: Grid Web App
 * File Created: Wednesday, 21st August 2019 12:51:45 PM
 * Author: nknab
 * Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
 * Version: 1.0
 * Brief: 
 * -----
 * Last Modified: Sunday, 25th August 2019 10:50:43 AM
 * Modified By: nknab
 * -----
 * Copyright ©2019 nknab
-->

<!DOCTYPE html>
<html lang="en">

<head>
	<!--Import css files-->
	<link type="text/css" rel="stylesheet" href="resources/css/style.css" media="screen,projection" />

	<!--Let browser know website is optimized for mobile-->
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta charset="UTF-8" />
	<meta http-equiv="X-UA-Compatible" content="ie=edge">

	<link rel="icon" type="image/png" href="resources/images/logo.png" />
	<title>Grid</title>
</head>

<body>

	<div id="loader">
		<div class="loading">
			<div class="obj"></div>
			<div class="obj"></div>
			<div class="obj"></div>
			<div class="obj"></div>
			<div class="obj"></div>
			<div class="obj"></div>
			<div class="obj"></div>
			<div class="obj"></div>
		</div>
	</div>

	<nav>
		<div class="icon">
			<img src="resources/images/logo.png">
		</div>

		<div class="text">
			<h1 class="verticalText">GRID</h1>
		</div>

		<div class="stop">
			<button class="icon-btn" id="stop"><img src="resources/images/icons/delete.png"></button>
			<p><span>Emergency</span><span>Stop</span></p>
		</div>
	</nav>

	<div class="gridPattern">


		<div class="grid">
			<table>
				<canvas id="mainCanvas">
					<tr>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid11">
									<img id="img-grid11" src="#" alt="Image">
								</canvas class="can">
							</div>
						</td>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid12">
									<img id="img-grid12" src="#" alt="Image">
								</canvas class="can">

							</div>
						</td>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid13">
									<img id="img-grid13" src="#" alt="Image">
								</canvas class="can">
							</div>
						</td>
					</tr>
					<tr>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid21">
									<img id="img-grid21" src="#" alt="Image">
								</canvas class="can">
							</div>
						</td>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid22">
									<img id="img-grid22" src="#" alt="Image">
								</canvas class="can">

							</div>
						</td>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid23">
									<img id="img-grid23" src="#" alt="Image">
								</canvas class="can">
							</div>
						</td>
					</tr>
					<tr>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid31">
									<img id="img-grid31" src="#" alt="Image">
								</canvas class="can">
							</div>
						</td>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid32">
									<img id="img-grid32" src="#" alt="Image">
								</canvas class="can">

							</div>
						</td>
						<td>
							<div class="gridCell">
								<canvas class="can" id="grid33">
									<img id="img-grid33" src="#" alt="Image">
								</canvas class="can">
							</div>
						</td>
					</tr>
				</canvas>
			</table>

		</div>


		<div class="stampsContainer">
			<div class="stamps">
				<img class="pattern" src="resources/images/patterns/pattern-one.png">
			</div>

			<div class="stamps">
				<img class="pattern" src="resources/images/patterns/pattern-two.png">
			</div>

			<div class="stamps">
				<img class="pattern" src="resources/images/patterns/pattern-three.png">
			</div>

			<div class="stamps">
				<img class="pattern" src="resources/images/patterns/pattern-four.png">
			</div>
		</div>
	</div>

	<div class="orderSpecs">
		<form>
			<div class="group">
				<input type="text" required="required" class="order-input-item" /><span class="bar"></span>
				<label>Design Name</label>
			</div>
			<div class="group">
				<input type="number" required="required" class="order-input-item" /><span class="bar"></span>
				<label>Quantity (yd)</label>
			</div>
			<div class="group">

				<div class="select">
					<select id="depots-list" class="select-text" required>
						<option value="" disabled selected></option>
						<option value="1">Option 1</option>
						<option value="2">Option 2</option>
						<option value="3">Option 3</option>
					</select>
					<span class="select-highlight"></span>
					<span class="select-bar"></span>
					<label class="select-label">Depot</label>
				</div>
			</div>
			<div class="btn-box">
				<button class="btn btn-cancel" id="cancelButton" type="button">Cancel</button>
				<button class="btn btn-submit" id="orderButton" type="button">Order</button>
			</div>
		</form>

	</div>
	<div class="flex-container">
		<div class="sectors">
			<h2>Sectors</h2>

			<table>
				<tr>
					<td>
						<div class="ppIcon"></div>
					</td>
					<td>
						<span id="pp">
							<h3>Production Plant</h3>
							<h4>192.168.0.100</h4>
						</span>
					</td>
					<td>
						<span>
							<button id="editButtonPP">
								<div class="editIcon"></div>
							</button>
							<p>Edit</p>
						</span>
					</td>
					<td>
						<span>
							<button id="testButtonPP">
								<div class="testIcon"></div>
							</button>
							<p>Test</p>
						</span>
					</td>
				</tr>
				<tr>
					<td>
						<div class="dbIcon"></div>
					</td>
					<td><span id="db">
							<h3>Delivery Bot</h3>
							<h4>192.168.0.200</h4>
						</span></td>
					<td>
						<span>
							<button id="editButtonDB">
								<div class="editIcon"></div>
							</button>
							<p>Edit</p>
						</span>
					</td>
					<td>
						<span>
							<button id="testButtonDB">
								<div class=" testIcon">
								</div>
							</button>
							<p>Test</p>
						</span>
					</td>
				</tr>

			</table>

		</div>
		<div class="order-header">
			<h2>Orders</h2>
		</div>
		<div class="orders">
			<div>
				<!-- <table id="orders-table"> -->
				<table class="mainTable">
					<tbody id="orders-table">
						<tr class=" rowLine">
							<td>
								<img src="resources/images/prints/print.jpg" alt="Avatar">
							</td>
							<td>
								<h3>AIX Print</h3>
								<table class="subTable">
									<tr>
										<td id="columnOne">
											<h4>Quantity: <strong>1500</strong> yards</h4>
										</td>
										<td id="columnTwo">
											<h4>Depot: <strong>2</strong></h4>
										</td>
									</tr>
								</table>

								<table class="subTable">
									<tr>
										<td id="idColumn">
											<h4>Order ID: <strong>0002</strong></h4>
										</td>
										<td id="statColumn">
											<h4 id="statusH4">Status: <strong id="status">Production</strong></h4>
										</td>
									</tr>
								</table>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<div class="orderProgress">
			<h2 id="orderName">Order Name</h2>

			<div class="orderProgTable">
				<table>
					<tr>
						<td>
							<span id="circle-production">
								<div class="circle">
									<img class="circle-image" src="resources/images/icons/fabric-gray.png">
								</div>
								<p>Production</p>
							</span>
						</td>
						<td>
							<div class="progress" id="bar1"></div>
						</td>
						<td>
							<span id="circle-delivery">
								<div class="circle">
									<img class="circle-image" src="resources/images/icons/delivery-truck-gray.png">
								</div>
								<p>Delivery</p>
							</span>
						</td>
						<td>
							<div class="progress" id="bar2"></div>
						</td>
						<td>
							<span id="circle-done">
								<div class="circle">
									<img class="circle-image" src="resources/images/icons/checked-gray.png">
								</div>
								<p>Done</p>
							</span>
						</td>
					</tr>
				</table>
				</table>
			</div>
		</div>


		<!-- The Modal -->
		<div id="editModal" class="modal">

			<!-- Modal content -->
			<div class="modal-content">
				<div class="modal-header">
					<span class="close">&times;</span>
					<h2 id="editModalHeader">Production Plant</h2>
				</div>
				<!-- <form> -->
				<div class="modal-body">

					<div id="ip">
					</div>

				</div>
				<div class="modal-footer">
					<div class="modal-btn-box">
						<button class="modal-btn modal-btn-cancel" id="modal-btn-cancel" type="button">Cancel</button>
						<button class="modal-btn modal-btn-submit" id="modal-btn-save" type="submit">Save</button>
					</div>
				</div>
				<!-- </form> -->
			</div>

		</div>



		<!-- <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script> -->
		<!-- <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script> -->
		<!-- <script src='http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js'></script> -->
		<script type="text/javascript" src="resources/js/jquery.min.js"></script>
		<script type="text/javascript" src="resources/js/jquery-ui.min.js"></script>
		<script type="text/javascript" src="resources/js/sweetalert.min.js"></script>
		<script type="text/javascript" src="resources/js/ipInput.js"></script>
		<script type="text/javascript" src="resources/js/script.js"></script>
</body>

</html>