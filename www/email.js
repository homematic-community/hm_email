/**
 * @file  email.js
 * @brief JavaScript-Funktionen für die E-Mail-Konfiguration.
 *
 * @author Harima-kun
 * @license Public Domain
 **/
 
/*############################################################################*/
/*# DOM-Funktionen                                                           #*/
/*############################################################################*/

/**
 * @fn $
 * @brief Alias für document.getElementById
 * 
 * @param id Id eines DOM-Elements.
 * @return DOM-Element
 */
$ = function(id)
{
  return document.getElementById(id);
};

/**
 * @fn hide
 * @brief Versteckt ein DOM-Element.
 *
 * @param element DOM-Element
 **/
hide = function(element) 
{
  element.style.display = "none";
};

/**
 * @fn show
 * @brief Macht ein DOM-Element sichtbar.
 *
 * @param element DOM-Element
 **/
show = function(element)
{
  element.style.display = "";
};

/*############################################################################*/
/*# Kommunikation (synchrones AJAX ;-) )                                     #*/
/*############################################################################*/

/**
 * @var xhr
 * @brief Kapselt die Erzeugung XMLHttpRequest-Objekts.
 **/
xhr =
{
  /**
   * @var m_create
   * @breif Browserspezifische Funktion zum Erzeugen des XMLHttpRequest-Objekts.
   **/
  m_create: null,
    
  /**
   * @fn create
   * @breif Erzeugt ein neues XMLHttpRequest-Objekt.
   *
   * Unterstüzt der Browser kein AJAX, wird eine entsprechende Exception
   * ausgelöst.
   *
   * @return Neues XMLHttpRequest-Objekt.
   **/
  create: function()
  {
    if (null == this.m_create)
    {
      this.init();
    }
      
    return this.m_create();
  },
      
  /**
   * @fn init
   * @brief Ermittelt, wie browserabhängig ein XMLHttpRequest-Objekt erzeugt
   *        werden kann.
   *
   * Falls der Browser kein AJAX unterstüzt, wird eine entsprechende Exception
   * ausgelöst.
   **/
  init: function()
  {
    var fn =
    [
      function() { return new XMLHttpRequest(); },
      function() { xmlHttp  = new ActiveXObject("Microsoft.XMLHTTP"); },
      function() { xmlHttp  = new ActiveXObject("Msxml2.XMLHTTP"); }
    ];
      
    for (var i = 0, len = fn.length; i < len; i++)
    {
      try        { fn[i]();}
      catch (ex) { continue; }
      this.m_create = fn[i];
      return;
    }
        
    if (null == this.m_create)
    {
      throw new Error("XMLHttpRequest not supported");
    }
      
  }
    
};

/**
 * @var http
 * @brief Kapselt HTTP-Operationen.
 **/
http =
{
  /**
   * @fn m_request
   * @brief Führt eine synchrone HTTP-Anfrage durch.
   *
   * @param method HTTP-Methode; "GET" oder "POST"
   * @param url    URL der HTTP-Ressource
   * @param data   Übertragene Daten (nur POST)
   *
   * @return Text der Antwort
   **/
  m_request: function(method, url, data)
  {
    var x = xhr.create();
    x.open(method, url, false);
    x.send(data);
    return x.responseText;
  },
      
  /**
   * @fn post
   * @brief Führt ein synchrones HTTP POST durch.
   *
   * @param url  URL der HTTP Ressource
   * @param data Zu übertragende Daten
   *
   * @return Text der Antwort
   **/
  post: function(url, data)
  {
    return this.m_request("POST", url, data);
  }
};

/*############################################################################*/
/*# DOM-Funktionen                                                           #*/
/*############################################################################*/

MainMenu = 
{
  _entries: 
  [
    {id: "mailMenuButton"   , tag: "mailContent"},
    {id: "accountMenuButton", tag: "accountContent"},
    {id: "tclMenuButton"    , tag: "tclContent"},
	{id: "testMenuButton"   , tag: "testContent"},
    {id: "infoMenuButton"   , tag: "infoContent"}
  ],

  _unselectEntry: function(entry)
  {
    $(entry.id).className = "menuButton";
    hide($(entry.tag));
  },
  
  _selectEntry: function(entry)
  {
    $(entry.id).className = "activeMenuButton";
    show($(entry.tag));
  },
  
  select: function(id)
  {
    for (var i = 0, len = this._entries.length; i < len; i++)
    {
      var entry = this._entries[i];
      if (id != entry.id)  { this._unselectEntry(entry); }
      else                 { this._selectEntry(entry); }
    }
  }
  
};

/*############################################################################*/
/*# Mail                                                                     #*/
/*############################################################################*/

/**
 * @constructor Mail
 * @brief Erzeugt eine neue E-Mail.
 *
 * @param mailData Initialdaten der E-Mail.
 **/
Mail = function(mailData)
{
  this.init(mailData);
};

/**
 * @const Mail.URL
 * @brief URL zum Speichern von E-Mails.
 **/
Mail.URL = "/addons/email/save.cgi?mail"

Mail.prototype =
{
  m_id: null,
  m_to: null,
  m_subject: null,
  m_content: null,
  m_tcl: false,
  
  /**
   * @fn init
   * @brief Initialisiert die E-Mail.
   *
   * @param mailData Initialdaten der E-Mail.
   **/
  init: function(mailData)
  {
    this.m_id = mailData["id"];
    this.m_to = mailData["to"];
    this.m_subject = mailData["subject"];
    this.m_content = mailData["content"];
    this.m_tcl = mailData["tcl"];
  },

  /**
   * @fn getId
   * @brief Liefert die Id der Mail
   **/
  getId: function()
  {
    return this.m_id;
  },
  
  /**
   * @fn show
   * @brief Zeigt die aktuellen Mail-Daten an.
   **/
  show: function()
  {
    $("toTextBox").value = this.m_to;
    $("subjectTextBox").value = this.m_subject;
    $("contentTextArea").value = this.m_content;
    $("tclCheckBox").checked = this.m_tcl;
  },
  
  /**
   * @fn save
   * @brief Speichert die aktuelle E-Mail.
   **/
  save: function()
  {
    this.m_to = $("toTextBox").value;
    this.m_subject = $("subjectTextBox").value;
    this.m_content = $("contentTextArea").value;
    this.m_tcl = $("tclCheckBox").checked;
    
    var data = "";
    data += "Id:"      + this.m_id + "\n";
    data += "To:"      + this.m_to + "\n";
    data += "Subject:" + this.m_subject + "\n";
    data += "Tcl:"     + this.m_tcl + "\n";
    data += "\n";
    data += this.m_content;
    
    var result = "AJAX error";
    try { result = http.post(Mail.URL, data); }
    catch (ex) { }
    if ("OK" == result) { alert("E-Mail wurde erfolgreich gespeichert!"); }
    else { alert("Fehler beim Speichern der E-Mail (" + result + ")!"); }
  }
  
};

/**
 * @var MailCollection
 * @brief Liste der verfügbaren E-Mails.
 **/
MailCollection = 
{
  m_mails: [],
  
  /**
   * @fn init
   * @brief Initialisiert die Liste und die Bildschirmausgabe.
   **/
  init: function()
  {
    this.m_mails = [];
    $("idListBox").innerHTML = "";
    
    for (var i = 0, len = Configuration.Mails.length; i < len; i++)
    {
      var mail = new Mail(Configuration.Mails[i]);
      this.m_mails.push(mail);
      
      var option = document.createElement("option");
      option.appendChild(document.createTextNode(mail.getId()));
      $("idListBox").appendChild(option);
    }
    
    // erstes Element anzeigen
    $("idListBox").selectedIndex = 0;
    this.show($("idListBox").firstChild);
  },
  
  /**
   * @fn show
   * @brief Zeigt die ausgewählte E-Mail an.
   **/
  show: function()
  {
    this.getSelectedMail().show();
  },
  
  /**
   * @fn getSelectedMail
   * @brief Liefert die ausgewählte E-Mail.
   **/
  getSelectedMail: function()
  {
    return this.m_mails[$("idListBox").selectedIndex];
  },
  
  /**
   * @fn saveSelectedMail
   * @brief Sichert die momentan angezeigte Mail.
   **/
  saveSelectedMail: function()
  {
    this.getSelectedMail().save();
  }
};

/*############################################################################*/
/*# E-Mail-Konto                                                             #*/
/*############################################################################*/

Account =
{
  URL: "/addons/email/save.cgi?account",
  
  init: function()
  {
    $("smtpTextBox").value = Configuration.Account["server"];
    $("fromTextBox").value = Configuration.Account["from"];
    $("authListBox").value = Configuration.Account["auth"];
    $("portTextBox").value = Configuration.Account["port"];
    $("tlsCheckBox").checked = Configuration.Account["tls"];
	$("starttlsCheckBox").checked = Configuration.Account["starttls"];
    $("userTextBox").value = Configuration.Account["username"];
    $("passwordTextBox").value = Configuration.Account["password"];
    $("password2TextBox").value = Configuration.Account["password"];
  },

  apply: function()
  {
    if ($("passwordTextBox").value == $("password2TextBox").value)
    {
      var data = ""
      data += "Server:" + $("smtpTextBox").value  + "\n";
      data += "From:" + $("fromTextBox").value + "\n";
      data += "Auth:" + $("authListBox").options[$("authListBox").selectedIndex].value + "\n";
	  data += "TLS:" + $("tlsCheckBox").checked + "\n";
	  data += "STARTTLS:" + $("starttlsCheckBox").checked + "\n";
      data += "User:" + $("userTextBox").value + "\n";
      data += "Password:" + $("passwordTextBox").value + "\n";
      data += "Port:" + $("portTextBox").value + "\n";
	  data += "\n";
    
      var result = "AJAX error";
      try { result = http.post(Account.URL, data); }
      catch (ex) { }
      if ("OK" == result) { alert("Kontodaten wurden erfolgreich gespeichert!"); }
      else { alert("Fehler beim Speichern der Kontodaten (" + result + ")!"); }
    }
    else
    {
      alert("Fehler: Passwort stimmt nicht überein");
    }
  }
  
};

/*############################################################################*/
/*# Tcl                                                                      #*/
/*############################################################################*/

/**
 * @var Tcl
 * @brief Kapselt Funktionen für das benutzerdefinierte Tcl Script.
 **/
Tcl =
{
  URL: "/addons/email/save.cgi?userScript",
  
  /**
   * @fn init
   * @brief Initialisiert die Ansicht des Tcl Scripts.
   **/
  init: function()
  {
    $("userScriptTextArea").value = Configuration.UserScript;
  },
  
  /**
   * @fn apply
   * @brief Speichert das Tcl Script.
   **/
  apply: function()
  {
    var data = "";
    data += "\n";
    data += $("userScriptTextArea").value;
    
    var result = "AJAX error";
    try { result = http.post(Tcl.URL, data); }
    catch (ex) { }
    if ("OK" == result) { alert("Tcl Script wurde erfolgreich gespeichert!"); }
    else { alert("Fehler beim Speichern des Tcl Scripts (" + result + ")!"); }
  }
};

/*############################################################################*/
/*# Testmail                                                                 #*/
/*############################################################################*/

Test =
{
  URL: "/addons/email/testmail.cgi?ID=1",
  
  /**
   * @fn apply
   * @brief Sendet eine Testmail
   **/
  apply: function()
  {
    var data = "";
    data += "\n";
    data += $("userScriptTextArea").value;
    
    var result = "AJAX error";
    try { result = http.m_request("GET", Test.URL, null); }
    catch (ex) { }
    if ("OK" == result) { alert("Testmail wurde gesendet!"); }
    else { alert("Fehler beim Senden der Email (" + result + ")!"); }
  }
};

/*############################################################################*/
/*# Einsprungpunkt                                                           #*/
/*############################################################################*/

/**
 * @fn startup
 * @brief Initialisiert die Anzeige.
 **/
startup = function()
{
  MailCollection.init();
  Account.init();
  Tcl.init();
  MainMenu.select("mailMenuButton");
};