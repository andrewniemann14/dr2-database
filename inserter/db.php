<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);



function connect() {
  // gets secure DB login information
  $db_info = parse_ini_file('/home2/niemann8/kiskis/database.ini');
  $hostname = $db_info["hostname"];
  $database = $db_info["dr2_database"];
  $username = $db_info["dr2_username"];
  $password = $db_info["dr2_password"];

  try {
    $pdo = new PDO("mysql:host=$hostname;dbname=$database", $username, $password);
    $dbo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); // PDO uses fake prepared statements by default
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Connection successful<br/>";
    return $pdo;
  } catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
  }
}


// identify challenge vs leaderboard, call function
function handleFile($pdo, $filename) {
  if (strpos($filename, "hallenges_2")) { // leaving off first letter so it doesn't return 0 (false)
    insertChallenges($pdo, $filename);
  } else if (strpos($filename, "eaderboards_2")) {
    insertLeaderboards($pdo, $filename);
  }
}


// INSERT CHALLENGES
function insertChallenges($pdo, $filename) {
  $stmtInsertChallenge = $pdo->prepare("INSERT INTO challenges VALUES (?, ?, ?, ?, ?)");
  
  try {
    $challengeJson = file_get_contents($filename);
    $challengeData = json_decode($challengeJson, true);
  
    $pdo->beginTransaction();
    foreach ($challengeData as $challenge) {
      $stmtInsertChallenge->execute([$challenge["id"], $challenge["start"], $challenge["end"], $challenge["stage"], $challenge["vehicle_class"]]);
      echo $challenge["id"];
      echo " inserted<br/>";
    }
    $pdo->commit();
    rename($filename, "./done/$filename");
  } catch (Exception $e) {
    $pdo->rollback();
    throw $e;
  }
}


// INSERT LEADERBOARDS
function insertLeaderboards($pdo, $filename) {
  $stmtInsertLeaderboard = $pdo->prepare("INSERT INTO leaderboard VALUES (?, ?, ?, ?, ?, ?, ?, ?)");

  try {
    $leaderboardJson = file_get_contents($filename);
    $leaderboardData = json_decode($leaderboardJson);

    $pdo->beginTransaction();
    foreach ($leaderboardData as $leaderboard) {
      $stmtInsertLeaderboard->execute($leaderboard);
    }
    $pdo->commit();
    rename($filename, "./done/$filename");
  } catch (Exception $e) {
    $pdo->rollback();
    throw $e;
  }
}