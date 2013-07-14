<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
    <link rel='stylesheet' type='text/css' href='<?cs var:style ?>' />
    <title>
        <?cs var:title ?>
    </title>
</head>
<body>
    <?cs include:"templates/header.cs"  ?>
    <?cs with:listables = pages ?>
        <?cs include:"templates/lister.cs"  ?>
    <?cs /with ?>
    <?cs include:"templates/footer.cs"  ?>
</body>
</html>
