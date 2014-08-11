package de.upb.upbmonitor.rest;

import org.apache.http.HttpResponse;

import android.util.Log;
import de.upb.upbmonitor.monitoring.model.UeContext;
import de.upb.upbmonitor.rest.RestAsyncRequest.RequestType;

public class UeEndpoint
{
	private static final String LTAG = "UeEndpoint";
	private String mUrl;

	public UeEndpoint(String host, int port)
	{
		this.mUrl = "http://" + host + ":" + port + "/api/ue";
		Log.v(LTAG, "Created endpoint: " + this.mUrl);
	}

	public void register(UeContext c)
	{
		class UePostRequest extends RestAsyncRequest
		{
			@Override
			protected void onPostExecute(HttpResponse response)
			{
				if (response == null)
					return;
				Log.i(LTAG, response.getStatusLine().toString());
				//TODO implement request result handling
				// response.getEntity().getContent()
			}
		}
		;
		UePostRequest r = new UePostRequest();
		r.setup(RequestType.POST, this.mUrl, c.toJson().toString());
		r.execute();
	}

	public void update(UeContext c)
	{

	}
	
	public void getAssignment(UeContext c)
	{
		
	}

	public void remove(UeContext c)
	{
		// this.delete("bla");
	}

}
