<?php require_once('lib/Parsedown.php');

class OwnCloud
{

    private function getNoteRaw($id)
    {
        $url = "http://api:api@owncloud.sinn.lan/index.php/apps/notes/api/v0.2/notes/". $id;
        $response = file_get_contents($url);
        return json_decode($response, true)['content'];
    }

    public function getMarkdownNote($id)
    {
        $Parsedown = new Parsedown();
        return $Parsedown->parse($this->getNoteRaw($id));
    }

    public function getHTMLNote($id)
    {
        return $this->getNoteRaw($id);
    }
}
