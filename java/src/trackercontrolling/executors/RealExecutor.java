package trackercontrolling.executors;

import smx.tracker.MeasurePointData;
import trackercontrolling.Tracker;
import trackercontrolling.PipeInterface;

public class RealExecutor implements CommandExecutor {
    private Tracker tracker;
    public RealExecutor() {
	this.tracker = new Tracker();
    }

    public String execute(String[] command) throws Exception {
	double r, theta, phi;
	String cmdword = command[0];
	if (cmdword.equals("connect")) {
	    this.tracker.connect();
	}
	else if (cmdword.equals("disconnect"))
	    this.tracker.disconnect();
	else if (cmdword.equals("move"))
	    this.tracker.move(new Double(command[1]),
			      new Double(command[2]),
			      new Double(command[3]));
	else if (cmdword.equals("move absolute"))
	    this.tracker.moveAbsolute(new Double(command[1]),
				       new Double(command[2]),
				       new Double(command[3]));
	else if (cmdword.equals("search"))
	    this.tracker.search(new Double(command[1]));
	else if (cmdword.equals("abort"))
	    this.tracker.abort();
	else if (cmdword.equals("home"))
	    this.tracker.home();
	else if (cmdword.equals("set mode")) {
	    String mode = command[1];
	    if (mode.equals("IFM"))
		this.tracker.setMeasureMode(Tracker.MeasureMode.IFM);
	    else if (mode.equals("ADM"))
		this.tracker.setMeasureMode(Tracker.MeasureMode.ADM);
	    else
		this.tracker.setMeasureMode(Tracker.MeasureMode.IFM_SET_BY_ADM);
	}
	else if (cmdword.equals("measure")) {
	    MeasurePointData m = this.tracker.measure(1)[0];
	    return Double.toString(m.distance())
		+" "+Double.toString(m.zenith())
		+" "+Double.toString(m.azimuth());
	}
	else
	    throw new RuntimeException(PipeInterface.UNRECOGNIZED);
	return "";
    }
}