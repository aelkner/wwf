<!DOCTYPE html>
<html>
<head>
    <style>
        input {
            margin-right: 6px;
        }
        a {
            padding-right: 2px;
            text-decoration: none;
        }
        a:visited {
            color: blue;
        }
    </style>
    <script type='text/javascript' src='/static/jquery.js'></script>
    <script type='text/javascript'>
        $(document).ready(function(){
            $(".field").focus(function(event) {
                $(this).select();
            });
            $(".field").keydown(function(event) {
                var key = event.keyCode;
                if (key == 38 || key == 40) {
                    var fields = Array('starts_with', 'ends_with', 'contains');
                    var index = fields.indexOf(this.id);
                    if (key == 38) {
                        index = index + 1;
                    } else {
                        index = index - 1;
                    }
                    index = (index + 3) % 3;
                    var newField = "#" + fields[index];
                    $(newField).focus();
                    event.preventDefault();
                }
            });
            $("#{{focus}}").focus();
        });
    </script>
</head>
<body>
    <h2>Words With Friends Filter Tool</h2>
    <form action="/" method="post">
        Starts with: <input id="starts_with" class="field" name="starts_with" type="text" value="{{form['starts_with']}}"/>
        Ends with: <input id="ends_with" class="field" name="ends_with" type="text" value="{{form['ends_with']}}" />
        Contains: <input id="contains" class="field" name="contains" type="text" value="{{form['contains']}}" />
        <input value="Filter" type="submit" />
    </form>
    <br>
    <div>
        % for bucket in buckets:
            % if bucket['words']:
            <div>
                {{bucket['heading']}}
                <br>
                % for word in bucket['words']:
                    <a href="http://www.thefreedictionary.com/{{word}}">{{word}}</a>
                % end
                <br>
                <br>
            </div>
            % end
        % end
    </div>
</body>
</html>
