

public class Floor {

	public int[][] array_map;
	Location guidance_light[];
	public int number_light;
	public int address[];

	public Floor(int row, int column, int number_light, int sensornumber) {
	array_map = new int [row][column];
	guidance_light = new Location[number_light];
	address = new int[sensornumber];
	}
	
	public int[][] get_map() {
		return this.array_map;
	}
	
	public int get_data(int x, int y) {
		return this.array_map[x][y];
	}

	public int get_number_light() {
		return this.number_light;
	}

	public void set_map(int x, int y, int num) {
		this.array_map[x][y] = num;
	}

	public void print(int x, int y) {
		for (int i = 0; i < x; i++) {
			System.out.println();
			for (int j = 0; j < y; j++) {
				System.out.print(this.array_map[i][j]);
			}
		}
	}

}
