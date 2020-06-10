package socket;

import gnu.io.CommPort;

import gnu.io.CommPortIdentifier;

import gnu.io.SerialPort;

import java.io.File;
import java.io.IOException;

import java.io.InputStream;

import java.io.OutputStream;

import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;

public class Serial {

	static SocketClient c;

	static long first_time = System.currentTimeMillis();

	static long second_time = System.currentTimeMillis();

	public Serial() {

		super();

	}

	void connect(String portName) throws Exception {

		CommPortIdentifier portIdentifier = CommPortIdentifier.getPortIdentifier(portName);

		if (portIdentifier.isCurrentlyOwned()) {

			System.out.println("Error: Port is currently in use");

		} else {

			// 클래스 이름을 식별자로 사용하여 포트 오픈

			CommPort commPort = portIdentifier.open(this.getClass().getName(), 2000);

			if (commPort instanceof SerialPort) {

				// 포트 설정(통신속도 설정. 기본 9600으로 사용)

				SerialPort serialPort = (SerialPort) commPort;

				serialPort.setSerialPortParams(9600, SerialPort.DATABITS_8, SerialPort.STOPBITS_1,

						SerialPort.PARITY_NONE);

				// Input,OutputStream 버퍼 생성 후 오픈

				InputStream in = serialPort.getInputStream();

				OutputStream out = serialPort.getOutputStream();

				// 읽기, 쓰기 쓰레드 작동

				(new Thread(new SerialReader(in))).start();

				(new Thread(new SerialWriter(out))).start();

			} else {

				System.out.println("Error: Only serial ports are handled by this example.");

			}

		}

	}

	/** */

	// 데이터 수신

	public static class SerialReader implements Runnable {

		InputStream in;

		public SerialReader(InputStream in) {

			this.in = in;

		}

		public void run() {

			byte[] buffer = new byte[1024];

			int len = -1;

			int value = 0;

			String str;
			String ip = "192.168.43.129";
			int port = 5777;
			File sound = new File("siren.wav");
			
			try {
				while ((len = this.in.read(buffer)) > -1) {

					str = new String(buffer, 0, len);
					if (!str.equals("")) {
						if(str.equals("2")) {
							mp3(sound);
						}
						value = value * 10 + Integer.parseInt(str);

					}

					if (value > 100000000) {

						System.out.println(value);

						c = new SocketClient(ip, port);
						c.startSocket(Integer.toString(value));

						value = 0;

					}

				}

			} catch (IOException e) {

				e.printStackTrace();

			}

		}

	}

	/** */

	// 데이터 송신

	public static class SerialWriter implements Runnable {

		OutputStream out;

		public SerialWriter(OutputStream out) {

			this.out = out;

		}

		public void run() {

			try {

				while (true) {

					second_time = System.currentTimeMillis();

					// System.out.println((second_time - first_time) / 1000);

					if ((second_time - first_time) / 1000 > 3) {

						this.out.write('r');

						first_time = second_time;

					}

				}

			} catch (IOException e) {

				e.printStackTrace();

			}

		}

	}
	
	public static void mp3(File sound) {
		try {
			Clip clip = AudioSystem.getClip();
			clip.open(AudioSystem.getAudioInputStream(sound));
			clip.start();
		}catch(Exception e) {
			System.out.println(e);
		}
	}
	

	public static void main(String[] args) {

		try {

			(new Serial()).connect("COM5"); // 입력한 포트로 연결

		} catch (Exception e) {

			// TODO Auto-generated catch block

			e.printStackTrace();

		}

	}

}