package de.upb.upbmonitor.commandline;

import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.TimeoutException;

import android.util.Log;

import com.stericson.RootTools.RootTools;
import com.stericson.RootTools.exceptions.RootDeniedException;
import com.stericson.RootTools.execution.Command;
import com.stericson.RootTools.execution.CommandCapture;

/**
 * Wraps the RootTools API in order to execute command line commands
 * in a blocking way.
 *  
 * @author manuel
 */
public class BlockingCommand
{
	private static final String LTAG = "BlockingCommand";
	private static ArrayList<String> output;
	
	public static ArrayList<String> execute(String... command)
	{
		return BlockingCommand.execute(true, command);
	}
	
	/**
	 * Executes command as root or not.
	 * Returns ArrayList<String> of its ooutputs.
	 * 
	 * @param asRoot
	 * @param command
	 * @return ArrayList<String>
	 */
	public static ArrayList<String> execute(boolean asRoot, String... command)
	{
		// create output array
		output = new ArrayList<String>();
		
		// define command
		Command cmd = new CommandCapture(0, false, command)
		{

			@Override
			public void commandCompleted(int id, int exitCode)
			{
				Log.i(LTAG, "Cmd: '" + this.getCommand().trim() + "' Exitcode: " + exitCode);
				this.notifyAll();
			}

			@Override
			public void commandOutput(int id, String line)
			{
				output.add(line);
			}

			@Override
			public void commandTerminated(int id, String reason)
			{
				this.notifyAll();
			}
		};
		try
		{
			// execute command
			RootTools.getShell(asRoot).add(cmd);
			
			// wait until command has finished
			synchronized (cmd)
			{
				cmd.wait();
			}
		} catch (IOException e)
		{
			e.printStackTrace();
		} catch (TimeoutException e)
		{
			e.printStackTrace();
		} catch (RootDeniedException e)
		{
			e.printStackTrace();
		} catch (InterruptedException e)
		{
			e.printStackTrace();
		}
		// return output lines of command
		return output;
	}
}
