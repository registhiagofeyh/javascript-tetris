<!DOCTYPE html>
<html>
<head>
  <title>Javascript Tetris</title>
  <link rel="stylesheet" type="text/css" href="/static/css/style.css">
</head>

<body>

  <div id="tetris">
    <div id="menu">
      <p id="start"><a href="javascript:play();">Pressione &lt;espaço&gt; para jogar</a></p>
      <p><canvas id="upcoming"></canvas></p>
      <p>Pontos <span id="score">00000</span></p>
      <p>Linhas <span id="rows">0</span></p>
    </div>
    <canvas id="canvas">
      Sorry, this example cannot be run because your browser does not support the &lt;canvas&gt; element
    </canvas>
  </div>

  <script src="/static/js/jquery-2.2.3.min.js"></script>
  <script src="/static/js/stats.js"></script>
  <script src="/static/js/game.js"></script>
  <script>
  var runInterval = null;
  function runGame() {
    getUpdatedBlocks();
    if (runInterval) clearInterval(runInterval);
    if (BlocksUpdated) {
      run();
    } else {
      runInterval = setInterval(runGame, 1000);
    }
  }

    runGame();
  </script>

</body>
</html>
