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
  if (strpos($filename, "hallenges_2")) { // leaving off first letter so it doesn't return 0 (false)
    try {
      insertChallenges($pdo, $dir, $filename);
    } catch (Exception $e) {
      echo $e->getMessage(); // catch the error so that duplicates are skipped instead of crashing the script (mostly for dev/debugging)
    }
  } else if (strpos($filename, "eaderboards_2")) {
    try {
      insertLeaderboards($pdo, $dir, $filename);
    } catch (Exception $e) {
      echo $e->getMessage();
    }
  }
}


// INSERT CHALLENGES
function insertChallenges($pdo, $dir, $filename) {
  $stmtInsertChallenge = $pdo->prepare("INSERT INTO challenges VALUES (?, ?, ?, ?, ?, ?)");
  
  try {
    $challengeJson = file_get_contents($dir.$filename);
    $challengeData = json_decode($challengeJson, true);
  
    $pdo->beginTransaction();
    foreach ($challengeData as $challenge) {
      $stmtInsertChallenge->execute([$challenge["id"], $challenge["start"], $challenge["end"], $challenge["country"], $challenge["stage"], $challenge["vehicle_class"]]);
      echo "Challenge #" .$challenge["id"]. " inserted\n";
    }
    $pdo->commit();
    rename($dir.$filename, $dir."backup/".$filename);
  } catch (Exception $e) {
    $pdo->rollback();
    throw $e;
  }
}


// INSERT LEADERBOARDS
function insertLeaderboards($pdo, $dir, $filename) {
  $stmtInsertLeaderboard = $pdo->prepare("INSERT INTO leaderboard VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");

  try {
    $leaderboardJson = file_get_contents($dir.$filename);
    $leaderboardData = json_decode($leaderboardJson);

    $pdo->beginTransaction();
    $i = null;
    foreach ($leaderboardData as $leaderboard) {
      $stmtInsertLeaderboard->execute($leaderboard);
      $i++;
    }
    echo "$i leaderboard entries inserted\n";
    $pdo->commit();
  } catch (Exception $e) {
    $pdo->rollback();
    throw $e;
  }
}