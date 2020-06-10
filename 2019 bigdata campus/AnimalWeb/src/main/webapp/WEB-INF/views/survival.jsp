<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"
	language="java"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ page session="false"%>
<!DOCTYPE html>
<html lang="en">

<!-- Basic -->
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">

<!-- Mobile Metas -->
<meta name="viewport"
	content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">

<!-- Site Metas -->
<title>왈왈왈🐶</title>
<meta name="keywords" content="">
<meta name="description" content="">
<meta name="author" content="">

<!-- Site Icons -->
<link rel="shortcut icon" href="resources/images/favicon.ico"
	type="image/x-icon" />
<link rel="apple-touch-icon"
	href="resources/images/apple-touch-icon.png">

<!-- Bootstrap CSS -->
<link rel="stylesheet" href="resources/css/bootstrap.min.css">
<!-- Site CSS -->
<link rel="stylesheet" href="resources/style.css">
<!-- Colors CSS -->
<link rel="stylesheet" href="resources/css/colors.css">
<!-- ALL VERSION CSS -->
<link rel="stylesheet" href="resources/css/versions.css">
<!-- Responsive CSS -->
<link rel="stylesheet" href="resources/css/responsive.css">
<!-- Custom CSS -->
<link rel="stylesheet" href="resources/css/custom.css">

</head>
<body class="animal_version">

	<!-- LOADER -->
	<div id="preloader">
		<div class="cube-wrapper">
			<div class="cube-folding">
				<span class="leaf1"></span> <span class="leaf2"></span> <span
					class="leaf3"></span> <span class="leaf4"></span>
			</div>
			<span class="loading" data-name="Loading">Loading</span>
		</div>
	</div>
	<!-- end loader -->
	<!-- END LOADER -->

	<div id="wrapper">

		<!-- Sidebar-wrapper -->
		<div id="sidebar-wrapper">
			<div class="side-top">
				<div class="logo-sidebar">
					<a href="index"><img src="resources/images/logos/logo.png"
						alt="image"></a>
				</div>
				<ul class="sidebar-nav">
					<li><a href="index">소개</a></li>
					<li><a class="active" href="about">예측</a></li>
					<li><a href="services">반려견</a></li>
					<li><a href="services2">유기견</a></li>
					<li><a href="shelter">주요장소</a></li>
					<li><a href="shelter2">관할기관</a></li>
				</ul>
			</div>
		</div>


		<!-- Page Content -->
		<div id="page-content-wrapper">
			<a href="#menu-toggle" class="menuopener" id="menu-toggle"><i
				class="fa fa-bars"></i></a>

			<div class="all-page-bar">
				<div class="container">
					<div class="row">
						<div class="col-xs-12 col-sm-12 col-md-12">
							<div class="title title-1 text-center">
								<div class="title--heading">
									<h1>결과</h1>
								</div>
								<div class="clearfix"></div>
								<ol class="breadcrumb">
									<li><a href="index">Home</a></li>
									<li class="active">결과</li>
								</ol>
							</div>
							<!-- .title end -->
						</div>
					</div>
				</div>
			</div>
		</div>

		<div id="services" class="section lb">
			<div class="container-fluid">
				<div class="section-title row text-center">
					<div class="col-md-8 col-md-offset-2">
						<!-- <small>WELCOME TO THE OUR animal SHOP</small> -->
						<h3>결 과</h3>
						<hr class="grd1">
					</div>
				</div>

				<div class="section wb">
					<div class="container-fluid">
						<div class="row">
							<div class="col-md-8 col-md-offset-2 text-center">
								<div class="message-box">
									<h2>${live}</h2>
									<br />
									<h2>${bye}</h2>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="section-title row text-center">
					<div class="col-md-8 col-md-offset-2">
						<br> <br>
						<h3>결과 해석</h3>
						<hr class="grd1">
					</div>
				</div>

				<div class="section wb">
					<div class="container-fluid">
						<div class="row">
							<div class="message-box text-center">
								<h2><strong>model</strong> : decision tree</h2>
								<h3><strong>data</strong> : 2015~2018 losted dogs</h3>
								<h3><strong>variable</strong> : age, weightCd, neuterYn, sgg</h3>
							</div> <hr>
							<div class="image-box text-center">
								<img src="resources/uploads/graph/graph3.png" alt="" width=90% /> <hr>
								<img src="resources/uploads/graph/graph1.png" alt="" width=100% /> <hr>
								<img src="resources/uploads/graph/graph2.png" alt="" width=100% />

							</div>
						</div>
					</div>
				</div>

			</div>
		</div>
		<!-- end container -->
	</div>
	<!-- end section -->


	<a href="#" id="scroll-to-top" class="dmtop global-radius"><i
		class="fa fa-angle-up"></i></a>

	<!-- ALL JS FILES -->
	<script src="${pageContext.request.contextPath}/resources/js/all.js"></script>
	<script
		src="${pageContext.request.contextPath}/resources/js/responsive-tabs.js"></script>
	<!-- ALL PLUGINS -->
	<script src="${pageContext.request.contextPath}/resources/js/custom.js"></script>

	<!-- Menu Toggle Script -->
	<script>
		(function($) {
			"use strict";
			$("#menu-toggle").click(function(e) {
				e.preventDefault();
				$("#wrapper").toggleClass("toggled");
			});
			smoothScroll.init({
				selector : '[data-scroll]', // Selector for links (must be a class, ID, data attribute, or element tag)
				selectorHeader : null, // Selector for fixed headers (must be a valid CSS selector) [optional]
				speed : 500, // Integer. How fast to complete the scroll in milliseconds
				easing : 'easeInOutCubic', // Easing pattern to use
				offset : 0, // Integer. How far to offset the scrolling anchor location in pixels
				callback : function(anchor, toggle) {
				} // Function to run after scrolling
			});
		})(jQuery);
	</script>

</body>
</html>