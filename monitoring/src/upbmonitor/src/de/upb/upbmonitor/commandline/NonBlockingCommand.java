package de.upb.upbmonitor.commandline;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import android.util.Log;

import com.stericson.RootTools.RootTools;
import com.stericson.RootTools.exceptions.RootDeniedException;
import com.stericson.RootTools.execution.Command;
import com.stericson.RootTools.execution.CommandCapture;

/**
 * Wraps the RootTools API in order to execute command line commands.
 *  
 * @author manuel
 */
public class NonBlockingCommand
{
	private static final String LTAG = "BlockingCommand";
	
	public static void execute(String... command)
	{
		NonBlockingCommand.execute(true, command);
	}
	
	/**
	 * Executes command as root or not.
	 * Returns ArrayList<String> of its ooutputs.
	 * 
	 * @param asRoot
	 * @param command
	 * @return ArrayList<String>
	 */
	public static void execute(boolean asRoot, String... command)
	{	
		// define command
		Command cmd = new CommandCapture(0, false, command)
		{

			@Override
			public void commandCompleted(int id, int exitCode)
			{
				Log.v(LTAG, "Cmd: '" + this.getCommand().trim() + "' Exitcode: " + exitCode);
				this.notifyAll();
			}

			@Override
			public void commandOutput(int id, String line)
			{
			}

			@Override
			public void commandTerminated(int id, String reason)
			{
			}
		};
		try
		{
			// execute command
			RootTools.getShell(asRoot).add(cmd);
			
		} catch (IOException e)
		{
			e.printStackTrace();
		} catch (TimeoutException e)
		{
			e.printStackTrace();
		} catch (RootDeniedException e)
		{
			e.printStackTrace();
		}
	}
}
