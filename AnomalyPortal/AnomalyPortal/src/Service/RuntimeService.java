package Service;

public class RuntimeService {
	public static void RunCommand(String command) {
		Runtime runtime = Runtime.getRuntime();
		try{
			runtime.exec(command);
		}catch(Exception e){
			System.out.println("Error!");
		}
	}
}
