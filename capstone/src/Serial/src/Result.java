

class Result {

	Shortcut result_s = new Shortcut();
	
	public Result(Floor floor, int row, int column, int number_light) {
		Shortcut[] result = new Shortcut[number_light];
		
		for (int i = 0; i < number_light; i++) {
			result[i] = new Shortcut();
			result[i].Shortcut(floor.get_map(), floor.guidance_light[i].x,
					floor.guidance_light[i].y, row, column, 8, 0, 7);
			result_s = result[i].result_shortcut(result_s,row,column);
		}
		
		result_s.print(row, column);
		System.out.println();
		System.out.println();
	}


	public Shortcut get_result() {
		return this.result_s;
	}
	
	public int get_num(int x, int y) {
		return this.result_s.get_num(x, y);
	}
	
}