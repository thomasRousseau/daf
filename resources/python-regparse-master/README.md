Python Registry Parser 
=======================
The idea of this started out as one to duplicate Microsoft's autoruns tool to the extent possible with only offline registry hives. Then I started adding extra non-autorun(ish) registry keys and then it turned into more of a Windows Registry parser; hence the name change from autoreg-parse to python-regparse. I'm terrible at naming scripts/tools so this will have to suffice.

I wrote about it here on my blog: https://sysforensics.org/2015/03/python-registry-parser.html

Purpose/Reason
===============
- I didn't like the output of other tools.
- I wanted to learn to write better Python code.

Output
=======
This was a sticky point I had with alternative tools, and realizing this I thought hard and came to the conclusion if I want a tool that doesn't have messy output i'm going to have to make it custom user defined output, and then provide a fallback template file if a custom output isn't defined via the command line. This will likely turn some people off from using this tool, but I think it's the best way forward.

I suggest taking a look here for some output examples: http://sysforensics.org/2015/03/python-registry-parser.html as it's not as complex as it may sound. Even for non-coders it's easy.

The template file are prebuilt output templates. More of people that aren't going to be sed/awk/greping output (like me) or maybe you just wanted a standard HTML output that you can use for reporting purposes.

        regparse.py --plugin typedurls --hives hives/ntuser.dat --format_file templates/typedurls.html
        
        2014-06-04 13:09:14.749073|url1|http://google.com/
        2014-06-04 13:09:14.749073|url3|chrome
        2014-06-04 13:09:14.749073|url4|http://go.microsoft.com/fwlink/?LinkId=69157

        python regparse.py --plugindetails
        
        <snip>
        TYPEDPATHS
        	Plugin: 	TYPEDPATHS
        	Author: 	Patrick Olsen
        	Version: 	0.2
        	Reference: 	http://sysforensics.org
        	Print Fields: 	"{{ last_write }}|{{ key }}|{{ value }}|{{ data }}"
        	Description: 	Parses the NTUSER hive and returns Typed Paths entries.
        TYPEDURLS
        	Plugin: 	TYPEDURLS
        	Author: 	Patrick Olsen
        	Version: 	0.4
        	Reference: 	http://sysforensics.org
        	Print Fields: 	"{{ last_write }}|{{ url_name }}|{{ url }}"
        	Description: 	Parses the NTUSER hives and returns Typed URL entries.
        <snip>

So you want to look at the typed urls. You will see from the plugindeails that you have a few printable fields to choose from (last_write, url_name, and url).

For demonstation purposes to show the flexability of the output let's say you just want the url.

        python regparse.py --plugin typedurls --hives hives/ntuser.dat --format '{{url}}'
        
        http://google.com/
        chrome
        http://go.microsoft.com/fwlink/?LinkId=69157

Let's say you have multiple NTUSER hives that you want to process. You can do that like this:

        python regparse.py --plugin typedurls --hives hives/ntuser.dat hives/xphive/NTUSER.DAT --format '{{url}}'
        
        http://google.com/
        chrome
        http://go.microsoft.com/fwlink/?LinkId=69157
        http://google.com/
        \\vmware-host\Shared Folders\MalwareLabTools
        http://www.microsoft.com/isapi/redir.dll?prd=ie&pver=6&ar=msnhome

Or let's say you wanted to put the word "hello_world:" in front of each url (for whatever reason).

        python regparse.py --plugin typedurls --hives hives/ntuser.dat hives/xphive/NTUSER.DAT --format 'hello_world:{{url}}'
        
        hello_world:http://google.com/
        hello_world:chrome
        hello_world:http://go.microsoft.com/fwlink/?LinkId=69157
        hello_world:http://google.com/
        hello_world:\\vmware-host\Shared Folders\MalwareLabTools
        hello_world:http://www.microsoft.com/isapi/redir.dll?prd=ie&pver=6&ar=msnhome

This allows you to tag the output, which you can then simply filter away at a later time.

Now if you want all of it you just re-add those printable fields as such:

        python regparse.py --plugin typedurls --hives hives/ntuser.dat hives/xphive/NTUSER.DAT --format "{{last_write}}|{{url_name}}|{{url}}"
        
        2014-06-04 13:09:14.749073|url1|http://google.com/
        2014-06-04 13:09:14.749073|url3|chrome
        2014-06-04 13:09:14.749073|url4|http://go.microsoft.com/fwlink/?LinkId=69157
        2014-09-05 05:21:12.234362|url1|http://google.com/
        2014-09-05 05:21:12.234362|url2|\\vmware-host\Shared Folders\MalwareLabTools
        2014-09-05 05:21:12.234362|url3|http://www.microsoft.com/isapi/redir.dll?prd=ie&pver=6&ar=msnhome

How to Install
===============
- Install Python 2.79
- Install https://pypi.python.org/pypi/setuptools
- sudo pip install python-registry
- sudo pip install jinja2
- wget https://github.com/sysforensics/python-regparse/archive/master.zip
- Unzip
- Put it where you want, and then enjoy!

I've tested/used on OSX, Windows and SIFT 3.0. If pip doesn't work for you try easy_install.

Want to Help?
==============
- If something is broke let me know.
- If you want a plugin let me know.
- Share hives. I only have so many to test against.
- Feel free to write some plugins.

Thanks to:
==============
@williballenthin - http://www.williballenthin.com for writing python-registry, which is what I am using under the hood and for the idea of using user defined output.

@hiddenillusion - This example got me started on the idea. https://github.com/williballenthin/python-registry/blob/master/samples/forensicating.py
