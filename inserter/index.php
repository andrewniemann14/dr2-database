<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DR2.0 Challenge Database Updater</title>
  <link rel="stylesheet" href="inserter.css">
</head>
<body>

  <div class="file-list">
    <h2>Files in Queue</h2>
    <?php
    foreach (scandir('.') as $filename) {
      if (strpos($filename, ".json")) {
        echo "$filename<br/>";
      }
    }
    ?>
  </div>
  
  <form action="index.php" method="post">
    <input type="submit" name="insertNow" value="insertNow" />
  </form>

  <?php
    include "db.php";
    
    // https://stackoverflow.com/questions/20738329/how-to-call-a-php-function-on-the-click-of-a-button
    if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST['insertNow']))
    {
      $pdo = connect();
      foreach (scandir('.') as $filename) {
        handleFile($pdo, $filename);
      }
    }
  ?>


</body>
</html>