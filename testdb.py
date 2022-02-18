# function connect() {
#   // gets secure DB login information
#   $db_info = parse_ini_file('/home2/niemann8/kiskis/database.ini');
#   $hostname = $db_info["hostname"];
#   $database = $db_info["dr2_add_database"];
#   $username = $db_info["dr2_add_username"];
#   $password = $db_info["dr2_add_password"];

#   try {
#     $pdo = new PDO("mysql:host=$hostname;dbname=$database", $username, $password);
#     $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); // PDO uses fake prepared statements by default
#     $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
#     echo "Connection successful<br/>";
#     return $pdo;
#   } catch(PDOException $e) {
#     echo "Connection failed: " . $e->getMessage();
#   }
# }

with open("/home2/niemann8/kiskis/database.ini") as f:
  print(f.read()) # this works