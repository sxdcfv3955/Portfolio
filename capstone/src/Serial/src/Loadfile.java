

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

class Loadfile {
	Floor floor;
	public Loadfile(String filepath, int row, int column, int number_light, int sensornumber) {
		floor = new Floor(row, column, number_light, sensornumber);
		int light = 0;
		try {
			File file = new File(filepath);
			Scanner fs = new Scanner(file);
			
			for (int i = 0; i < row; i++) {
				for (int j = 0; j < column; j++) {
					floor.set_map(i, j, fs.nextInt());
					if (floor.get_data(i, j) == 8) {
						floor.set_map(i, j, 0);
						floor.guidance_light[light] = new Location();
						floor.guidance_light[light].set_Location(i,j);
						light++;
					}
				}
			}

		} catch (FileNotFoundException e) {
			System.out.println("error-> " + e);
		}
	}

	Floor get_floor() {
		return this.floor;
	}
}