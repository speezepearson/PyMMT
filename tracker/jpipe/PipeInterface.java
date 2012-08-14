import java.io.IOException;
import java.io.InputStreamReader;
import java.io.BufferedReader;

public class PipeInterface {
    public static final String IDENT = "subprocess_identifier";
    public static final String DELIMITER = "\t";
    public static final String SUCCESS = "success";
    public static final String ERROR = "error";
    public static final String UNRECOGNIZED = "unrecognized";
    public static BufferedReader cin = 
	new BufferedReader(new InputStreamReader(System.in));

    public static int countLines(String s) {
	int result = 1;
	for (int i=s.indexOf('\n'); i != -1; i = s.indexOf('\n', i+1))
	    result += 1;
	return result;
    }

    public static String getCommand() throws IOException {
	return cin.readLine();
    }

    public static void printResponse(String command, String status,
				     String response) {
	if (status.equals(UNRECOGNIZED))
	    System.out.println(IDENT+DELIMITER+command+DELIMITER
			       +status+DELIMITER+"0");
	else {
	    System.out.println(IDENT+DELIMITER+command+DELIMITER
			       +status+DELIMITER+countLines(response));
	    System.out.println(response);
	}
    }

    public static void readExecuteWrite(CommandExecutor executor) throws IOException {
	String command, status, response;
	command = cin.readLine();
	try {
	    response = executor.execute(command);
	    status = SUCCESS;
	} catch (Exception e) {
	    response = e.getMessage();
	    if (e.getMessage().equals(UNRECOGNIZED))
		status = UNRECOGNIZED;
	    else
		status = ERROR;
	}
	printResponse(command, status, response);
    }
}