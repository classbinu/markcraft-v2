window.convertHtmlToMarkdown = function (html) {
  const turndownService = new TurndownService();
  // 헤더 태그에 대한 사용자 정의 규칙
  // 헤더 태그에 대한 사용자 정의 규칙
  turndownService.addRule("headers", {
    filter: ["h1", "h2", "h3", "h4", "h5", "h6"],
    replacement: function (content, node) {
      let prefix = "#"; // 기본적으로 h1은 #
      if (node.nodeName === "H2") {
        prefix = "##";
      } else if (node.nodeName === "H3") {
        prefix = "###";
      } else if (node.nodeName === "H4") {
        prefix = "####";
      } else if (node.nodeName === "H5") {
        prefix = "#####";
      } else if (node.nodeName === "H6") {
        prefix = "######";
      }
      // h4, h5, h6 등에 대한 처리도 추가할 수 있습니다.

      return prefix + " " + content + "\n\n";
    },
  });
  // <br> 태그와 리스트 항목에 대한 사용자 정의 규칙
  turndownService.addRule("breaks", {
    filter: ["br"],
    replacement: function (content, node) {
      if (node.nodeName === "BR") {
        return `&lt;br&gt;`; // <br> 태그에 대한 개행
      }
      return content;
    },
  });
  // <br>, <ul>, <ol>, <p> 태그에 대한 사용자 정의 규칙
  turndownService.addRule("customFormatting", {
    filter: ["ul", "ol", "hr"],
    replacement: function (content, node) {
      if (node.nodeName === "UL" || node.nodeName === "OL") {
        // 리스트 항목 사이에 개행 문자 추가
        return content.split("\n").join("<br>");
      }
      if (node.nodeName === "HR") {
        // 수평선을 만났을 때
        return "<br>***<br>";
      }
      return content;
    },
  });
  const resp = turndownService.turndown(html);

  return resp;
};
