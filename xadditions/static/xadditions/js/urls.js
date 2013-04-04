//
// script from https://github.com/mlouro/django-js-utils/
//

var dutils = {};
dutils.conf = {};

dutils.urls = function(){

    function _get_path(name, kwargs, urls)
    {

        var path = urls[name] || false;

        if (!path)
        {
            throw('URL not found for view: ' + name);
        }

        var _path = path;

        var key;
        for (key in kwargs)
        {
            if (kwargs.hasOwnProperty(key)) {
                if (!path.match('<' + key +'>'))
                {
                    throw(key + ' does not exist in ' + _path);
                }
                path = path.replace('<' + key +'>', kwargs[key]);
            }
        }

        var re = new RegExp('<[a-zA-Z0-9-_]{1,}>', 'g');
        var missing_args = path.match(re);
        if (missing_args)
        {
            throw('Missing arguments (' + missing_args.join(", ") + ') for url ' + _path);
        }

        return path;

    }

    return {

        resolve: function(name, kwargs, urls) {
            if (!urls)
            {
                urls = X_ALL_URLS || {};
            }

            return _get_path(name, kwargs, urls);
        }

    };

}();
