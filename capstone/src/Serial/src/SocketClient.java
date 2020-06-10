// ������ �����Ͽ� 10���ڸ� ������.

import java.io.*;
import java.net.*;
import java.util.*;

public class SocketClient {
	
	// ������ ����� ���� �ν��Ͻ���
	private Socket socket=null;
	
	// ���Ͽ��� ��Ʈ���� ������ ���� �ν��Ͻ���
	private OutputStream os = null;
	private OutputStreamWriter writer = null;		
	

	// ������. �־��� IP�� ��Ʈ��ȣ�� ������ �����Ѵ�.
	public SocketClient(String ip, int port) throws IOException {

		try {		
			// ���� ������ �����ϰ�, Ŭ���̾�Ʈ���� ��Ʈ���� �޾Ƶ帱 ������ �ϳ� �� �����մϴ�.
			socket=new Socket(ip, port);
			System.out.println("������ �����Ͽ� ������ �����Ͽ����ϴ�.");			
		} catch (IOException e) { 
			throw e;
		}
	}
	
	public void startSocket(String ars) {
		String str=ars;
		
		try {		
			
			// ���Ͽ� ��Ʈ���� �����ϰ�, ��Ʈ���� ���� Writer�� ����ϴ�.
			os = socket.getOutputStream();
			writer = new OutputStreamWriter(os);

		} catch (IOException e) {
			System.out.println("���� ���ῡ �����߽��ϴ�.");
		}
		
		try {
			writer.write(str);
			writer.flush();
		} catch (IOException e) { 
			System.out.println("������ ���ۿ� �����߽��ϴ�.");
		}
		
		System.out.println("���� ������:"+str);
		
		try {
			socket.close();
			writer.close();			
			os.close();
		} catch (IOException e) {
			System.out.println("���� �ݱ⿡ �����߽��ϴ�");
		}
	}	
}
