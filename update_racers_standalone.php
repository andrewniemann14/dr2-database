<!-- php /home2/niemann8/dr2-data/update_racers_standalone.php -->

<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$pdo = connect();

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


$all_names = array();
$stmt = $pdo->prepare("SELECT DISTINCT name FROM leaderboard");
$stmt->execute();
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
  array_push($all_names, $row['name']);
}

$already_names = array();
$stmt = $pdo->prepare("SELECT DISTINCT name FROM racers");
$stmt->execute();
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
  array_push($already_names, $row['name']);
}

$names_to_add = array_diff($all_names, $already_names);


$i = 0;
// for each name in array, query ALL entries and insert/update to database

print(count($names_to_add));

foreach ($names_to_add as $name) {
  $stmtSelect = $pdo->prepare("SELECT nationality, score, AVG(score) FROM leaderboard WHERE name = ?");
  $stmtSelect->execute(array($name));

  $points = 0;

  $first_row = $stmtSelect->fetch(PDO::FETCH_ASSOC);
  $nationality = $first_row['nationality'];
  $score = $first_row['AVG(score)'];
  $points += $first_row['score'];
  while ($row = $stmtSelect->fetch(PDO::FETCH_ASSOC)) {
    $points += $row['score'];
  }
  
  $stmtUpdate = $pdo->prepare("INSERT INTO racers VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE points = points + ?, score = ?");
  $stmtUpdate->execute(array($name, $nationality, $points, $score, $points, $score));
  print(++$i.'_');
}