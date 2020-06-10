// 서버에 연결하여 10글자를 보낸다.

import java.io.*;
import java.net.*;
import java.util.*;

public class SocketClient {
	
	// 소켓을 만들기 위한 인스턴스들
	private Socket socket=null;
	
	// 소켓에서 스트림을 얻어오기 위한 인스턴스들
	private OutputStream os = null;
	private OutputStreamWriter writer = null;		
	

	// 생성자. 주어진 IP와 포트번호로 소켓을 생성한다.
	public SocketClient(String ip, int port) throws IOException {

		try {		
			// 서버 소켓을 생성하고, 클라이언트에서 스트림을 받아드릴 소켓을 하나 더 생성합니다.
			socket=new Socket(ip, port);
			System.out.println("소켓을 생성하여 서버와 연결하였습니다.");			
		} catch (IOException e) { 
			throw e;
		}
	}
	
	public void startSocket(String ars) {
		String str=ars;
		
		try {		
			
			// 소켓에 스트림을 연결하고, 스트림을 보낼 Writer를 만듭니다.
			os = socket.getOutputStream();
			writer = new OutputStreamWriter(os);

		} catch (IOException e) {
			System.out.println("소켓 연결에 실패했습니다.");
		}
		
		try {
			writer.write(str);
			writer.flush();
		} catch (IOException e) { 
			System.out.println("데이터 전송에 실패했습니다.");
		}
		
		System.out.println("보낸 데이터:"+str);
		
		try {
			socket.close();
			writer.close();			
			os.close();
		} catch (IOException e) {
			System.out.println("소켓 닫기에 실패했습니다");
		}
	}	
}
