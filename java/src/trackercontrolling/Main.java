package trackercontrolling;

import java.io.IOException;
import trackercontrolling.executors.CommandExecutor;
import trackercontrolling.executors.RealExecutor;
import trackercontrolling.executors.DummyExecutor;

public class Main {
    public static void main(String[] args) throws Exception {
        CommandExecutor executor;

        if (args.length > 0 && args[0].equals("dummy")) {
	    executor = new DummyExecutor();
	}
        else
            executor = new RealExecutor();

	while (true)
	    try {
		PipeInterface.readExecuteWrite(executor);
	    } catch (IOException e) {
	    } catch (NullPointerException e) {
		break;
	    }
    }
}