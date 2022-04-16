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

function check_for_valid_name($element) {
  return ($element[2] != 'DiRT Player' && $element[2] != '');
}

// identify challenge vs leaderboard, call function
function handleFile($pdo, $dir, $filename) {
  if (strpos($filename, "eaderboards_2")) {
    try {
      $names = updatePlayerPoints($pdo, $dir, $filename);
      updatePlayerScores($pdo, $names);
      rename($dir.$filename, $dir."backup/".$filename);
    } catch (Exception $e) {
      echo $e->getMessage();
    }
  }
}



function updatePlayerPoints($pdo, $dir, $filename) {
  try {
    $leaderboardJson = file_get_contents($dir.$filename);
    $leaderboardData = json_decode($leaderboardJson);

    $entries_to_score = array_filter($leaderboardData, "check_for_valid_name");

    $stmt = $pdo->prepare("INSERT INTO players VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE points = points + ?");
    $names_to_update = array();

    // for each entry/name in yesterday's challenge results:
    foreach ($entries_to_score as $entry) {
      $name = $entry[2];
      array_push($names_to_update, $name);
      $nationality = $entry[3];
      $points = $entry[8];

      $stmt->execute(array($name, $nationality, $points, $points, $points));
    }
    return $names_to_update;
  } catch (Exception $e) {
    throw $e;
  }
}

function updatePlayerScores($pdo, $names) {
  $scores = array();
  $stmt = $pdo->prepare("SELECT AVG(score) FROM leaderboard WHERE name = ?");
  try {

    // calculates the score for each name and stores it in a PHP array
    foreach ($names as $name) {
      $stmt->execute(array($name));
      $only_row = $stmt->fetch(PDO::FETCH_ASSOC);
      $score = $only_row['AVG(score)'];
      array_push($scores, $score);
    }

    // feeds that PHP array into a MySQL prepared statement
    $names_and_scores = array_combine($names, $scores);
    $stmt = $pdo->prepare("UPDATE players SET score = ? WHERE name = ?");
    $pdo->beginTransaction();
    foreach ($names_and_scores as $name_score_pair) {
      $stmt->execute(array($name_score_pair[0], $name_score_pair[1]));
    }
    $pdo->commit();
    echo(count($names_and_scores).' names updated');
  } catch (Exception $e) {
    throw $e;
  }
}

?>