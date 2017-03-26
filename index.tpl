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
            $("#starts_with, #ends_with, #contains").focus(function(event) {
                $(this).select();
            });
            $("#{{focus}}").focus();
        });
    </script>
</head>
<body>
    <h2>{{title}}</h2>
    <form action="/" method="post">
        Starts with: <input id="starts_with" name="starts_with" type="text" value="{{starts_with}}"/>
        Ends with: <input id="ends_with" name="ends_with" type="text" value="{{ends_with}}" />
        Contains: <input id="contains" name="contains" type="text" value="{{contains}}" />
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
                    <a href="http://www.merriam-webster.com/dictionary/{{word}}">{{word}}</a>
                % end
                <br>
                <br>
            </div>
            % end
        % end
    </div>
</body>
</html>
