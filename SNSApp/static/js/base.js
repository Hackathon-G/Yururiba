var img_src = new Array("../../images/character_pome.png", "../../images/pome_happy.png");
    var i = 0;
      function henkou() {

        if (i == 2) {
          i = 0;
        } else {
          i ++;
        }
        document.getElementById(“image_file”).src = img_src[i];
      }