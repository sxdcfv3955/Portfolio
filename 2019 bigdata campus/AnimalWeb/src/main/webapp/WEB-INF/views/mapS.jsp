<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ page import="java.sql.DriverManager"%>
<%@ page import="java.sql.Connection"%>
<%@ page import="java.sql.PreparedStatement"%>
<%@ page import="java.sql.ResultSet"%>

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>카카오맵테스트입니당</title>

</head>
<body>

	<div id="map" style="width: 100%; height: 600px;"></div>

	<script type="text/javascript"
		src="//dapi.kakao.com/v2/maps/sdk.js?appkey=3e896e211c4f04d9741451486d226571"></script>
	<script>
		var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
		mapOption = {
			center : new kakao.maps.LatLng(37.5650172,126.8494648), // 지도의 중심좌표
			level : 10
		// 지도의 확대 레벨
		};

		var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
	<%Connection conn = null;
			String driver = "oracle.jdbc.driver.OracleDriver";
			String url = "jdbc:oracle:thin:@localhost:1521:xe";

			Class.forName(driver);
			conn = DriverManager.getConnection(url, "WAL", "1234");
			String quary = "SELECT * FROM FACILITY";
			PreparedStatement pstm = conn.prepareStatement(quary);
			ResultSet rs = pstm.executeQuery();
			String name;
			double lat;
			double lng;
			while (rs.next()) {
				name = rs.getString(1).replace("/ufeff", "");
				lat = rs.getDouble(3);
				lng = rs.getDouble(2);%>
		var markerPosition = new kakao.maps.LatLng(
	<%=lat%>
		,
	<%=lng%>
		);

		// 마커를 생성합니다
		var marker = new kakao.maps.Marker({
			position : markerPosition
		});

		marker.setMap(map);
	<%}%>
		
	<%quary = "SELECT * FROM DRUG";
			pstm = conn.prepareStatement(quary);
			rs = pstm.executeQuery();
			while (rs.next()) {
				name = rs.getString(1).replace("/ufeff", "");
				lat = rs.getDouble(2);
				lng = rs.getDouble(3);%>
		var imageSrc = "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
		var imageSize = new kakao.maps.Size(24, 35);
		var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);
		var markerPosition = new kakao.maps.LatLng(
	<%=lat%>
		,
	<%=lng%>
		);

		// 마커를 생성합니다
		var marker = new kakao.maps.Marker({
			position : markerPosition,
			image : markerImage
		});

		marker.setMap(map);
	<%}%>
		
	</script>
</body>
</html>