/*
import gnu.io.CommPort;
import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileDescriptor;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.Scanner;

public class Main {
	static Floor floor[];
	static Result result;

	public static void main(String[] args) {
		// Main test = new Main();
		Serial serial = new Serial();
		try {
			serial.connect("COM5", "COM16");
			System.out.println("------");

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		int sensorID;
		int number_floor;
		Date date = new Date();

		Properties properties = new Properties();
		try {
			properties.load(new FileInputStream("C:/Users/sxdcf/eclipse-workspace/serial/info.properties"));

			floor = new Floor[Integer.parseInt(properties.getProperty("number.floor"))];

			for (int i = 1; i <= Integer.parseInt(properties.getProperty("number.floor")); i++) {
				floor[i - 1] = new Loadfile(
						properties.getProperty("directory") + properties.getProperty("floor" + i + ".mapfile"),
						Integer.parseInt(properties.getProperty("floor" + i + ".row")),
						Integer.parseInt(properties.getProperty("floor" + i + ".column")),
						Integer.parseInt(properties.getProperty("floor" + i + ".number_light")),
						Integer.parseInt(properties.getProperty("floor" + i + ".sensornumber"))).get_floor();

				// for (int j = 0; j < Integer.parseInt(properties.getProperty("floor" + i +
				// ".sensornumber")); j++)
				// floor[i - 1].address[j] = 0;
			}

			System.out.println("Success");
		} catch (

		IOException e) {
			System.out.println("error-> " + e);
		}

		for (int i = 1; i < Integer.parseInt(properties.getProperty("number.floor")); i++) {
			result = new Result(floor[i - 1], Integer.parseInt(properties.getProperty("floor" + i + ".row")),
					Integer.parseInt(properties.getProperty("floor" + i + ".column")),
					Integer.parseInt(properties.getProperty("floor" + i + ".number_light")));

			// System.out.println();
			// System.out.println();
		}

		sensorID = 1;

		SimpleDateFormat transFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		String sdate = transFormat.format(date);

		File logfile = new File(properties.getProperty("directory") + "log.txt");
		try {
			BufferedWriter write = new BufferedWriter(new FileWriter(logfile, true));
			write.write(sdate + " " + properties.getProperty("sensor" + sensorID + ".x") + " "
					+ properties.getProperty("sensor" + sensorID + ".y"));
			write.newLine();
			write.flush();

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		number_floor = Integer.parseInt(properties.getProperty("sensor" + sensorID + ".floor"));
		floor[number_floor - 1].set_map(Integer.parseInt(properties.getProperty("sensor" + sensorID + ".x")),
				Integer.parseInt(properties.getProperty("sensor" + sensorID + ".y")), 1);
		result = new Result(floor[number_floor - 1],
				Integer.parseInt(properties.getProperty("floor" + number_floor + ".row")),
				Integer.parseInt(properties.getProperty("floor" + number_floor + ".column")),
				Integer.parseInt(properties.getProperty("floor" + number_floor + ".number_light")));

		// System.out.println(result.get_num(11,10));

		// System.out.println();

		System.out.println("success2");
		int ID = 0;

	}

}

*/