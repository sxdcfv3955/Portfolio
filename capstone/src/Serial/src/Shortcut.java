
class Shortcut {
	public int Max_dist = 10000;
	public int[][] short_cut = new int[1000][1000];

	public boolean Shortcut(int[][] array_map, int x, int y, int row, int column, int start, int dist, int direc) {
		if (x < 0 || y < 0 || x >= row || y >= column
				|| (array_map[x][y] != 0 && array_map[x][y] != 8 && array_map[x][y] != 9)) {
			return false;
		}

		else {
			if (array_map[x][y] == 9) {
				if (Max_dist > dist) {
					for (int i = 0; i < row; i++) {
						for (int j = 0; j < column; j++) {
							short_cut[i][j] = array_map[i][j];
						}
					}
					Max_dist = dist;
				}
				return false;
			}

			if (direc == 2)
				array_map[x +1][y] = start;
			if (direc == 3)
				array_map[x][y-1] = start;
			if (direc == 4)
				array_map[x - 1][y] = start;
			if (direc == 5)
				array_map[x][y+1] = start;
			else
				array_map[x][y] = start;

			if (Shortcut(array_map, x - 1, y, row, column, 2, dist + 1, 2) != false
					|| Shortcut(array_map, x + 1, y, row, column, 4, dist + 1, 4) != false
					|| Shortcut(array_map, x, y + 1, row, column, 3, dist + 1, 3) != false
					|| Shortcut(array_map, x, y - 1, row, column, 5, dist + 1, 5) != false) {
				return true;
			}

			array_map[x][y] = 0;
			dist = dist - 1;

			return false;
		}
	}

	public int[][] get_shortcut() {
		return this.short_cut;
	}

	public int get_num(int x, int y) {
		return this.short_cut[x][y];
	}

	public void set_num(int x, int y, int num) {
		this.short_cut[x][y] = num;
	}

	public Shortcut result_shortcut(Shortcut result, int row, int column) {
		for (int i = 0; i < row; i++) {
			for (int j = 0; j < column; j++) {
				if ((result.get_num(i, j) < this.short_cut[i][j]))
					result.set_num(i, j, this.short_cut[i][j]);
			}
		}

		return result;
	}

	public void print(int x, int y) {
		for (int i = 0; i < x; i++) {
			System.out.println();
			for (int j = 0; j < y; j++) {
				System.out.print(this.short_cut[i][j]);
			}
		}
	}
}