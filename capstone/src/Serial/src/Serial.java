
import gnu.io.CommPort;
import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;

import java.io.FileDescriptor;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class Serial {
	static int data;
	static OutputStream out;

	public Serial() {
		super();
	}

	void connect(String OUTportName) throws Exception {
		CommPortIdentifier OUTportIdentifier = CommPortIdentifier.getPortIdentifier(OUTportName);
		if (OUTportIdentifier.isCurrentlyOwned()) {
			System.out.println("Error: Port is currently in use");
		} else {
			CommPort OUTcommPort = OUTportIdentifier.open(this.getClass().getName(), 2000);

			if (OUTcommPort instanceof SerialPort) {
				SerialPort OUTserialPort = (SerialPort) OUTcommPort;
				OUTserialPort.setSerialPortParams(9600, SerialPort.DATABITS_8, SerialPort.STOPBITS_1,
						SerialPort.PARITY_NONE);

				out = OUTserialPort.getOutputStream();

				(new Thread(new SerialWriter(out))).start();

			} else {
				System.out.println("Error: Only serial ports are handled by this example.");
			}
		}
	}

	public void input(int x) {
		int value = 0;
		try {
			for (int i = 1; i < 9; i++) {
				value = (9-i) * 10 + x % 10;
				x = x / 10;
				this.out.write(value);
				//System.out.print("Send data : ");
				//System.out.println(value);
			}
			value = 0;

		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static class SerialWriter implements Runnable {
		OutputStream out;

		public SerialWriter(OutputStream out) {
			this.out = out;
		}

		public void run() {
			try {
				int c = 0;
				int value = 0;
				while (data > -1) {

					for (int i = 1; i < 9; i++) {
						value = (9-i) * 10 + data % 10;
						data = data / 10;
						this.out.write(value);
						
					}
					data = -1;
					value = 0;
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	static int get_data() {
		return data;
	}

	static void set_data(int x) {
		data = x;
	}
}