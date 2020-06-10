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
					<li><a class="active" href="index">소개</a></li>
					<li><a href="about">예측</a></li>
					<li><a href="services">반려견</a></li>
					<li><a href="services2">유기견</a></li>
					<li><a href="shelter">주요장소</a></li>
					<li><a href="shelter2">관할기관</a></li>
				</ul>
			</div>
		</div>

		<div id="page-content-wrapper">
			<a href="#menu-toggle" class="menuopener" id="menu-toggle"><i
				class="fa fa-bars"></i></a>

			<div id="home" class="parallax first-section"
				data-stellar-background-ratio="0.4"
				style="background-image: url('resources/uploads/animal_slider.jpg');">

				<div class="big-tagline text-center">
					<h2>
						<strong>찾아라 유기견</strong><br> made by WWW🐶
					</h2>
					<p class="lead">김호영 | 변호영 | 이호영</p>
				</div>
			</div>
			
			
			<div class="section wb">
				<div class="container-fluid">
					<div class="row">
						<div class="col-md-8 col-md-offset-2 text-center">
							<div class="message-box">
								<h4>ABOUT</h4>
								<h2>WELCOME TO W W W</h2>
								<p class="lead">유기된 동물의 왈왈왈(WWW) 울음소리를 표현한 소리입니다.</p>

								<h3><strong>예측</strong> : 유기된 동물의 입양 여부를 예측해주는 서비스</h3>
								<h3><strong>반려견</strong> : 전국 등록동물의 분포 (2015년 ~ 2018년)</h3>
								<h3><strong>유기견</strong> : 전국 유기동물의 분포 (2015년 ~ 2018년)</h3>
								<h3><strong>주요장소</strong> : 주요 유기동물 발생 장소</h3>
								<h3><strong>관할기관</strong> : 유기동물보호소, 동물약국, 동물병원의 위치</h3>
								<p>동물의 각종 편의시설까지!</p>
								<p>안내해 드립니다</p>
								
								
								<jsp:include page="graph.jsp"></jsp:include>
							</div>
						</div>
					</div>
					<hr class="hr1">
				</div>
			</div>

			<div id="animals" class="section lb">
				<div class="container-fluid">
					<div class="section-title row text-center">
						<div class="col-md-8 col-md-offset-2">
							<small>W W W</small>
							<h3>팀원 소개</h3>
							<hr class="grd1">
							<p class="lead">김호영 | 변경수 | 이민수</p>
						</div>
					</div>
					<!-- end title -->

					<div class="row dev-list text-center">
						<div class="col-lg-4 col-md-4 col-sm-12 col-xs-12 wow fadeIn"
							data-wow-duration="1s" data-wow-delay="0.2s">
							<div class="widget clearfix">
								<div class="hover-br"></div>
								<img src="resources/uploads/profile/kim.jpg" alt=""
									class="img-responsive">
								<div class="widget-title">
									<h3>HoYeong Kim</h3>
									<small>하이</small>

								</div>
							</div>
						</div>

						<div class="col-lg-4 col-md-4 col-sm-12 col-xs-12 wow fadeIn"
							data-wow-duration="1s" data-wow-delay="0.4s">
							<div class="widget clearfix">
								<div class="hover-br"></div>
								<img src="resources/uploads/profile/byun.jpg" alt=""
									class="img-responsive">
								<div class="widget-title">
									<h3>KyeongSu Byun</h3>
									<small>22살</small>
									<p>부경대학교 4학년</p>
								</div>
							</div>
						</div>

						<div class="col-lg-4 col-md-4 col-sm-12 col-xs-12 wow fadeIn"
							data-wow-duration="1s" data-wow-delay="0.6s">
							<div class="widget clearfix">
								<div class="hover-br"></div>
								<img src="resources/uploads/profile/lee.jpg" alt=""
									class="img-responsive">
								<div class="widget-title">
									<h3>MinSu Lee</h3>
									<small>바이</small>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<a href="#" id="scroll-to-top" class="dmtop global-radius"><i
		class="fa fa-angle-up"></i></a>

	<!-- ALL JS FILES -->
	<script src="resources/js/all.js"></script>
	<script src="resources/js/responsive-tabs.js"></script>
	<!-- ALL PLUGINS -->
	<script src="resources/js/custom.js"></script>

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