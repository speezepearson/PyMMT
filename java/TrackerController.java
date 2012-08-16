import java.io.IOException;

public class TrackerController {
    public static void main(String[] args) {
	CommandExecutor executor = new TrackerExecutor();
	while (true)
	    try {
		PipeInterface.readExecuteWrite(executor);
	    } catch (IOException e) {
	    } catch (NullPointerException e) {
		break;
	    }
    }
}