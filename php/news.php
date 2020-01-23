<script type="text/javascript">
      var $marquee = document.getElementById('marquee');
      var marquee = window.m = new dynamicMarquee.Marquee($marquee, { rate: -100 });


	  var obj = JSON.parse(testy);
      window.l = dynamicMarquee.loop(marquee, [
        function() { return obj.name; },
        function() { return 'It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old'; },
        function() { return 'Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the morrce'; },
        function() { return 'RLorem Ipsum comescero, written in 45 BC'; }
      ], function() {
        var $separator = document.createElement('div');
        $separator.innerHTML = '&nbsp|&nbsp';
        return $separator;
      });
	  </script>