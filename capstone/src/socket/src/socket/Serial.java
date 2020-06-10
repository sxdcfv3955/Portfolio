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

			// Ŭ���� �̸��� �ĺ��ڷ� ����Ͽ� ��Ʈ ����

			CommPort commPort = portIdentifier.open(this.getClass().getName(), 2000);

			if (commPort instanceof SerialPort) {

				// ��Ʈ ����(��żӵ� ����. �⺻ 9600���� ���)

				SerialPort serialPort = (SerialPort) commPort;

				serialPort.setSerialPortParams(9600, SerialPort.DATABITS_8, SerialPort.STOPBITS_1,

						SerialPort.PARITY_NONE);

				// Input,OutputStream ���� ���� �� ����

				InputStream in = serialPort.getInputStream();

				OutputStream out = serialPort.getOutputStream();

				// �б�, ���� ������ �۵�

				(new Thread(new SerialReader(in))).start();

				(new Thread(new SerialWriter(out))).start();

			} else {

				System.out.println("Error: Only serial ports are handled by this example.");

			}

		}

	}

	/** */

	// ������ ����

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

	// ������ �۽�

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

			(new Serial()).connect("COM5"); // �Է��� ��Ʈ�� ����

		} catch (Exception e) {

			// TODO Auto-generated catch block

			e.printStackTrace();

		}

	}

}