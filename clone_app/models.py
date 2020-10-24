from django.db import models
from django.contrib.auth.models import User



class images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()


class story(models.Model):
    


    startingTemplate = '''
        <div class="innerStoryCard" style="overflow:hidden;"></div><!--i-->
        <ul class="nav d-block storyContentControl storyContentControl-oneColor">
            <li class="nav-item">
                <a data-toggle="dropdown" class="nav-link text-white storyContentControl-navlink" style="text-align: center; line-height: 1;" href="#!"><i class="fas fa-palette"></i></a>
                <ul class="dropdown-menu">
                    <li class="nav-item p-3">
                        <ul class="nav d-block p-2">
                            <ul class="nav row" style="width: max-content">
                                <small class="text-muted">set text color</small>
                                <br/>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="white"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="black"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="grey"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="blue"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="cyan"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="purple"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="violet"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="lightblue"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="red"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextColor(this)" class="nav-link datacolorBtn" href="#!" data-color="green"></a>
                                </li>
                            </ul>
                            <li class="nav-item p-3">
                                <small class="text-muted">Custom Color</small>
                                <div class="d-flex">
                                    <div>
                                        #
                                    </div>
                                    <input onkeyup="setTextCustomColor(this)" style="border: none; border-bottom: 2px solid dodgerblue; width: 100%;" placeholder="Hex color code" maxlength="6" type="text">
                                </div>
                            </li>
                            <hr>
                            <ul class="nav row" style="width: max-content">
                                <small class="text-muted">Set layout color</small>
                                <br/>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="white"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="black"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="grey"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="blue"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="cyan"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="purple"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="violet"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="lightblue"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="red"></a>
                                </li>
                                <li class="nav-item">
                                    <a onclick="setTextSecondaryColor(this)" class="nav-link datacolorBtn" href="#!" data-color="green"></a>
                                </li>
                            </ul>
                        </ul>
                    </li>
                </ul>
            </li>
            <li class="nav-item pt-1">
                <a data-toggle="dropdown" class="nav-link text-white storyContentControl-navlink" style="text-align: center;" href="#!"><i class="fas fa-align-center"></i></a>
                <ul class="dropdown-menu">
                    <li class="nav-item p-3">
                        <ul class="nav d-flex justify-content-between" style="width: max-content;">
                            <li class="nav-item">
                                <a onclick="setTextAlign(this)" data-align="left" href="#!" class="nav-link btn text-info"><i class="fas fa-align-left"></i></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setTextAlign(this)" data-align="center" href="#!" class="nav-link btn text-info"><i class="fas fa-align-center"></i></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setTextAlign(this)" data-align="right" href="#!" class="nav-link btn text-info"><i class="fas fa-align-right"></i></a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li class="nav-item pt-1">
                <a data-toggle="dropdown" class="nav-link text-white storyContentControl-navlink" style="text-align: center;" href="#!"><i class="fas fa-quote-left"></i></a>
                <ul class="dropdown-menu">
                    <li class="nav-item p-3">
                        <small class="text-muted">Enter text</small>
                        <div class="d-block">
                            <input onkeyup="setText(this,'0')" style="border: none; border-bottom: 2px solid dodgerblue; width: 100%;" placeholder="Your text" type="text">
                            <div class="d-block threeInuptSpecialTextCase">
                                <input onkeyup="setText(this,'1')" style="border: none; border-bottom: 2px solid dodgerblue; width: 100%;" placeholder="Your text" type="text">
                                <input onkeyup="setText(this,'2')" style="border: none; border-bottom: 2px solid dodgerblue; width: 100%;" placeholder="Your text" type="text">
                            </div>
                        </div>
                    </li>
                </ul>
            </li>
            <li class="nav-item pt-1">
                <a data-toggle="dropdown" class="nav-link text-white storyContentControl-navlink" style="text-align: center;" href="#!"><i class="fas fa-font"></i></a>
                <ul class="dropdown-menu" style="width: max-content;">
                    <li class="nav-item p-3">
                        <a href="#!" onclick="setTextFont(this)" class="nav-link" style='font-family: Georgia, serif;' data-font="Georgia, serif">Nice mood under moon light</a>
                    </li>
                    <li class="nav-item p-3">
                        <a href="#!" onclick="setTextFont(this)" class="nav-link" style='font-family: Arial, Helvetica, sans-serif;' data-font="Arial, Helvetica, sans-serif">Nice mood under moon light</a>
                    </li>
                    <li class="nav-item p-3">
                        <a href="#!" onclick="setTextFont(this)" class="nav-link" style='font-family: "Comic Sans MS", cursive, sans-serif;' data-font='"Comic Sans MS", cursive, sans-serif'>Nice mood under moon light</a>
                    </li>
                    <li class="nav-item p-3">
                        <a href="#!" onclick="setTextFont(this)" class="nav-link" style='font-family: "Courier New", Courier, monospace;' data-font='"Courier New", Courier, monospace'>Nice mood under moon light</a>
                    </li>
                </ul>
            </li>
            <li class="nav-item pt-1">
                <a data-toggle="dropdown" class="nav-link text-white storyContentControl-navlink" style="text-align: center;" href="#!"><i class="fas fa-sync-alt"></i></a>
                <ul class="dropdown-menu">
                    <li class="nav-item p-3">
                        <input type="range" onmousemove="setRotationDegree(this)" class="form-control">
                    </li>
                </ul>
            </li>
            <li class="nav-item pt-1">
                <a data-toggle="dropdown" class="nav-link text-white storyContentControl-navlink" style="text-align: center;" href="#!"><i class="fas fa-text-width"></i></a>
                <ul class="dropdown-menu">
                    <li class="nav-item p-3">
                        <input type="range" onmousemove="setFontSize(this)" class="form-control">
                    </li>
                </ul>
            </li>
            <li class="nav-item pt-1">
                <a onclick="removeEditableContainer()" class="nav-link text-white storyContentControl-navlink" style="text-align: center;" href="#!"><i class="fas fa-trash"></i></a>
            </li>
        </ul>
        <ul class="storyControls nav d-flex justify-content-between">
            <li class="nav-item">
                <a onclick="removeStory(this)" href="#!" class="nav-link"><i class="fas fa-trash"></i></a>
            </li>
            <li class="nav-item">
                <a data-toggle="dropdown" class="nav-link"><i class="fas fa-circle"></i></a>
                <ul class="dropdown-menu p-3">
                    <li class="nav-item">
                        <ul class="nav row p-2" style="width: 100%;">
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="white"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="black"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="grey"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="blue"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="cyan"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="purple"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="violet"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="lightblue"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="red"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="green"></a>
                            </li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <small class="text-muted">Custom Color</small>
                        <div class="d-flex">
                            <div>
                                #
                            </div>
                            <input onkeyup="setStoryCustomBg(this)" style="border: none; border-bottom: 2px solid dodgerblue; width: 100%;" placeholder="Hex color code" maxlength="6" type="text">
                        </div>
                    </li>
                    <li class="nav-item">
                        <smal class="text-muted">Pre-made gradients</smal>
                        <ul class="nav row p-2" style="width: 100%;">
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, white, grey)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, black, grey)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, blue, violet)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, green, yellow)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, red, darkred)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, dodgerblue, green)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, violet, red)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, green, cyan)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, white, cyan)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, pink, violet)"></a>
                            </li>
                            <li class="nav-item">
                                <a onclick="setStoryBg(this)" class="nav-link datacolorBtn" href="#!" data-color="linear-gradient(90deg, pink, red)"></a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    story = models.TextField(default=startingTemplate)
    story_images = models.ManyToManyField(images)
    views = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

