<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$dir = '/home2/niemann8/dr2-data/';

$pdo = connect();
foreach (scandir($dir) as $filename) {
  handleFile($pdo, $dir, $filename);
}

function connect() {
  // gets secure DB login information
  $db_info = parse_ini_file('/home2/niemann8/kiskis/database.ini');
  $hostname = $db_info["hostname"];
  $database = $db_info["dr2_add_database"];
  $username = $db_info["dr2_add_username"];
  $password = $db_info["dr2_add_password"];

  try {
    $pdo = new PDO("mysql:host=$hostname;dbname=$database", $username, $password);
    $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); // PDO uses fake prepared statements by default
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Connection successful\n";
    return $pdo;
  } catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
  }
}

// identify challenge vs leaderboard, call function
function handleFile($pdo, $dir, $filename) {
  if (strpos($filename, "eaderboards_2")) {
    try {
      $names = updateRacerPoints($pdo, $dir, $filename);
      updateRacerScores($pdo, $names);
      rename($dir.$filename, $dir."backup/".$filename);
    } catch (Exception $e) {
      echo $e->getMessage();
    }
  }
}



function updateRacerPoints($pdo, $dir, $filename) {
  try {
    $leaderboardJson = file_get_contents($dir.$filename);
    $leaderboardData = json_decode($leaderboardJson);

    function check_for_valid_name($element) {
      return ($element[2] != 'DiRT Player' && $element[2] != '');
    }
    $entries_to_score = array_filter($leaderboardData, "check_for_valid_name");

    $stmt = $pdo->prepare("INSERT INTO racers VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE points = points + ?");
    $names_to_update = array();

    // for each entry/name in yesterday's challenge results:
    foreach ($entries_to_score as $entry) {
      $name = $entry[2];
      array_push($names_to_update, $name);
      $nationality = $entry[3];
      $points = $entry[8];

      // INSERT: this should work
      // UPDATE: points are updated but new score is not yet calculated
      $stmt->execute(array($name, $nationality, $points, $points, $points));
    }
    return $names_to_update;
  } catch (Exception $e) {
    throw $e;
  }
}

function updateRacerScores($pdo, $names) {
  try {
    foreach ($names as $name) {
      $stmt = $pdo->prepare("SELECT AVG(score) FROM leaderboard WHERE name = ?");
      $stmt->execute(array($name));
      $only_row = $stmt->fetch(PDO::FETCH_ASSOC);
      $score = $only_row['AVG(score)'];
  
      $stmt = $pdo->prepare("UPDATE racers SET score = ? WHERE name = ?");
      $stmt->execute(array($score, $name));
    }
  } catch (Exception $e) {
    throw $e;
  }
}

?>