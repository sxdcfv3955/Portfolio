
// 소켓을 하나 열어서 클라이언트 소켓에서 10글자를 얻어오고 소켓을 닫는다.

import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.*;

public class SocketServer {
	static Floor floor[];
	static Result result;
	static Serial conn;
	static int default_address = 111111111;
	static int pre_address = default_address;
	

	static int[] pre_arr= new int[] {1,1,1,1,1,1,1,1,1};
	static int[] new_arr= new int[9];

	static int direction_data;
	static Date date = new Date();

	private ServerSocket serverSocket = null;
	private Socket socket = null;

	private InputStream is = null;
	private InputStreamReader reader = null;

	public SocketServer(int port) throws IOException {
		try {
			serverSocket = new ServerSocket(port);
			System.out.println("Making socket & Wait, Port Num : " + port);
			socket = serverSocket.accept();
			System.out.println("Connect client");
		} catch (IOException e) {
			throw e;
		}
	}

	public void startSocket() {
		int sensorID;
		int number_floor;
		String str = "";

		try {
			is = socket.getInputStream();
			reader = new InputStreamReader(is);
		} catch (IOException e) {
			System.out.println(e);
		}
		for (int i = 0; i < 9; i++) {
			try {
				str = str + (char) reader.read();
			} catch (IOException e) {
				System.out.println(e);
			}
		}
		System.out.println("Input Data (address) : " + str);
		int new_address = Integer.parseInt(str);
		System.out.print("new address : ");
		System.out.println(new_address);
		System.out.print("pre address : ");
		System.out.println(pre_address);
		pre_address = new_address;
		for(int i=0; i<9; i++) {
			new_arr[8-i]=new_address%10;
			new_address/=10;
		}
		
		for(int id=0; id<9; id++) {
		if (pre_arr[id] != new_arr[id]) {
			pre_arr[id] = new_arr[id];
			
			sensorID = id+1;
			System.out.print("Sensor ID : ");
			System.out.println(sensorID);

			Properties properties2 = new Properties();
			try {
				FileInputStream file2 = new FileInputStream("C:/Users/sxdcf/eclipse-workspace/serial/info.properties");
				properties2.load(file2);

				SimpleDateFormat transFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
				String sdate = transFormat.format(date);

				File logfile = new File(properties2.getProperty("directory") + "log.txt");
				try {
					BufferedWriter write = new BufferedWriter(new FileWriter(logfile, true));
					write.write(sdate + " " + properties2.getProperty("sensor" + sensorID + ".x") + " "
							+ properties2.getProperty("sensor" + sensorID + ".y"));
					write.newLine();
					write.flush();
					System.out.println("Success Write Log File");

				} catch (IOException e) {
					e.printStackTrace();
				}

				number_floor = Integer.parseInt(properties2.getProperty("sensor" + sensorID + ".floor"));
				floor[number_floor - 1].set_map(Integer.parseInt(properties2.getProperty("sensor" + sensorID + ".x")),
						Integer.parseInt(properties2.getProperty("sensor" + sensorID + ".y")), 1);
				result = new Result(floor[number_floor - 1],
						Integer.parseInt(properties2.getProperty("floor" + number_floor + ".row")),
						Integer.parseInt(properties2.getProperty("floor" + number_floor + ".column")),
						Integer.parseInt(properties2.getProperty("floor" + number_floor + ".number_light")));

				direction_data = 0;
				for (int i = 0; i < Integer
						.parseInt(properties2.getProperty("floor" + number_floor + ".number_light")); i++) {
					direction_data = direction_data * 10
							+ result.get_num(floor[number_floor - 1].guidance_light[i].get_x(),
									floor[number_floor - 1].guidance_light[i].get_y());
				}

				System.out.print("Output Data (direction) : ");
				System.out.println(direction_data);
				conn.input(direction_data);

				System.out.println("Success Input");

				file2.close();
			} catch (IOException e) {
				System.out.println(e);
			}
		}
	}
		try {
			serverSocket.close();
			socket.close();
			reader.close();
			is.close();
		} catch (IOException e) {
			System.out.println(e);
		}

	}

	public static void main(String args[]) {
		SocketServer s;
		int port = 5777;

		Properties properties = new Properties();
		try {
			FileInputStream file = new FileInputStream("C:/Users/sxdcf/eclipse-workspace/serial/info.properties");
			properties.load(file);
			floor = new Floor[Integer.parseInt(properties.getProperty("number.floor"))];

			for (int i = 1; i <= Integer.parseInt(properties.getProperty("number.floor")); i++) {
				floor[i - 1] = new Loadfile(
						properties.getProperty("directory") + properties.getProperty("floor" + i + ".mapfile"),
						Integer.parseInt(properties.getProperty("floor" + i + ".row")),
						Integer.parseInt(properties.getProperty("floor" + i + ".column")),
						Integer.parseInt(properties.getProperty("floor" + i + ".number_light")),
						Integer.parseInt(properties.getProperty("floor" + i + ".sensornumber"))).get_floor();

			}

			for (int i = 1; i < Integer.parseInt(properties.getProperty("number.floor")); i++) {
				result = new Result(floor[i - 1], Integer.parseInt(properties.getProperty("floor" + i + ".row")),
						Integer.parseInt(properties.getProperty("floor" + i + ".column")),
						Integer.parseInt(properties.getProperty("floor" + i + ".number_light")));
			}

			direction_data = 0;
			for (int i = 0; i < Integer.parseInt(properties.getProperty("floor" + 1 + ".number_light")); i++) {
				direction_data = direction_data * 10
						+ result.get_num(floor[0].guidance_light[i].get_x(), floor[0].guidance_light[i].get_y());

			}
			
			System.out.println("Success loading file");

			file.close();

		} catch (IOException e) {
			System.out.println(e);
		}

		if (args.length > 0) {
			port = Integer.parseInt(args[0]);
		}

		try {
			conn = new Serial();

			System.out.println("Success socket");
			try {
				conn.connect("COM23");

				System.out.println("Success COMport");
			} catch (Exception e) {
				e.printStackTrace();
			}
			conn.input(777777777);
			while (true) {
				s = new SocketServer(port);
				s.startSocket();
			}
		} catch (IOException e) {
			System.out.println(e);
		}
	}
}