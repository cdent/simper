<?cs each:comment = comments ?>
<div class="comment">
    <h3><a href="/content/name/<?cs var:comment.name ?>">
        <?cs var:comment.name ?></a>
    </h3>
    <div class="commenttime"><?cs var:comment.mod_time ?></div>
    <div class="commentcontent">
        <?cs var:comment.content ?>
    </div>
    <div class="commentcomments">
    <ul>
    <?cs each:associate = comment.associates ?>
        <li><a href="/content/name/<?cs var:associate.name ?>">
            <?cs var:associate.name ?></a></li>
    <?cs /each ?>
    </ul>
    </div>
</div>
<?cs /each ?>
