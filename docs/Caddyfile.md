#### About
##### Here are Caddyfile examples, that have been tested, but do not work as needed

```
admin.play.buerokratt.ee {
    reverse_proxy /treening/treening/teemad* http://admin.play.buerokratt.ee:3001

    @static {
        file
        path_regexp .*
        not path /treening/treening/teemad* 
    }

#    route @static {
#        root * /opt/html/training-module/assets
#        file_server browse
#    }

#    route {
#        try_files {path} /opt/html/training-module/index.html
#        reverse_proxy /training/* http://admin.play.buerokratt.ee:3001
#    }

    handle_path /treening/treening/teemad* {
        root * /opt/html/training-module
        file_server browse
        header Content-Type text/html 
    }

    handle_path /assets/index-6c58ad83.js* {
	root * /opt/html/training-module
	file_server browse
	header Content-Type application/javascript
    }

    handle_path /assets/index-3bb525d2.css* {
        root * /opt/html/training-module
        file_server browse
        header Content-Type text/css
    }


    handle {
         reverse_proxy /* http://admin.play.buerokratt.ee:3006
    }
}

```
