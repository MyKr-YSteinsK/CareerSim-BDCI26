"use strict";
let state = null;
let pending = false;
const $ = id => document.getElementById(id);
const stats = [["health","Health · 健康"],["dignity","Dignity · 尊严"],["skill","Skill · 技能"],["network","Network · 人脉"],["output","Output · 产出"],["wealth","Wealth · 财富"],["energy","Energy · 精力"]];
function text(id, value) { $(id).textContent = value ?? "—"; }
function render(next) {
  state = next;
  const facts = state.facts;
  const current = facts.state || {};
  text("mode", state.mode);
  text("timeline", facts.state ? `Year ${current.year ?? "—"} / Quarter ${current.quarter ?? "—"} / Month ${current.month ?? "—"} / ${current.level ?? "—"}` : "准备开始");
  text("notice", state.error || state.rejection || "");
  $("start-panel").hidden = state.phase !== "START";
  $("game-panel").hidden = state.phase === "START";
  const fixture = state.mode === "FIXTURE / NON_GAME";
  text("start-copy", fixture ? "FIXTURE / NON_GAME：演示选项不会创建真实游戏，合成数据包单独保存。" : "仅在获得 Human Run 授权后开始。启动页面本身不会创建游戏。请保留技术失败资料。");
  text("start", fixture ? "开始离线演示" : "开始人工对局");
  $("start").disabled = pending || state.start_available === false;
  $("stats").replaceChildren(...stats.map(([key,label]) => {
    const row = document.createElement("div"), dt = document.createElement("dt"), dd = document.createElement("dd");
    dt.textContent = label; dd.textContent = current[key] ?? "—"; row.append(dt,dd); return row;
  }));
  text("event-title", facts.event?.title || (state.phase === "ENDED" ? "对局结束" : "当前事件"));
  text("event-text", facts.event?.description || "");
  text("warning", facts.warning || "");
  text("handbook-text", facts.handbook || "开始后显示公开入职手册。");
  $("choices").replaceChildren(...state.choices.map(choice => {
    const button = document.createElement("button"), detail = document.createElement("small");
    button.append(document.createTextNode(choice.action));
    detail.textContent = choice.disabled_reason || `精力成本 ${choice.energy_cost ?? "未公开"}`;
    button.append(detail);
    button.disabled = pending || state.phase !== "ACTIVE" || Boolean(choice.disabled_reason);
    button.addEventListener("click", () => operation("choose", {choice:choice.choice, revision:state.revision, run_id:state.run_id}));
    return button;
  }));
  $("ending").hidden = state.phase !== "ENDED";
  text("result", Object.entries(facts.final_result || {}).map(([k,v]) => `${k}: ${v}`).join("\n"));
  text("export-status", state.export_message);
  $("download").hidden = !state.export_name;
  $("retry-export").hidden = state.finalization_status !== "EXPORT_FAILED_RETAINED";
  $("retry-export").disabled = pending;
  $("history-list").replaceChildren(...state.history.map(item => { const li=document.createElement("li"); li.textContent=item.action; return li; }));
}
async function operation(name, body={}) {
  if (pending || !state) return;
  pending = true; render(state);
  try {
    const response = await fetch(`/api/${name}`, {method:"POST",headers:{"Content-Type":"application/json","X-HPL-Token":state.token},body:JSON.stringify({...body,request_id:crypto.randomUUID()})});
    const result = await response.json();
    if (result.state) render(result.state);
    else throw Error(result.error || result.status);
    if (name === "shutdown" && result.accepted) text("notice","客户端已关闭，可以关闭此页面。");
  } catch (_) {
    text("notice", "连接或操作结果未知：不要重复提交动作。保留本局资料，返回 review。");
    // Freeze this page after an uncertain response; never auto-retry a mutation.
    $("choices").querySelectorAll("button").forEach(button => button.disabled=true);
    $("start").disabled=true;
    return;
  }
  pending = false; render(state);
  if (name === "shutdown") { pending=true; text("notice","客户端已关闭，可以关闭此页面。"); }
}
$("start").addEventListener("click", () => operation("start", {participant:$("participant").value}));
$("shutdown").addEventListener("click", () => operation("shutdown"));
$("retry-export").addEventListener("click", () => operation("export"));
$("handbook-open").addEventListener("click", () => $("handbook").showModal());
$("handbook-close").addEventListener("click", () => $("handbook").close());
$("history-open").addEventListener("click", () => $("history").showModal());
$("history-close").addEventListener("click", () => $("history").close());
$("download").addEventListener("click", async () => {
  try {
    const response=await fetch("/api/export", {headers:{"X-HPL-Token":state.token}});
    if (!response.ok) throw Error("export unavailable");
    const url=URL.createObjectURL(await response.blob()), link=document.createElement("a");
    link.href=url; link.download=state.export_name; link.click(); setTimeout(()=>URL.revokeObjectURL(url),1000);
  } catch (_) { text("notice","数据包暂不可下载，已保存的数据仍保留。请返回 review。"); }
});
fetch("/api/state").then(response=>response.json()).then(render).catch(()=>text("notice","无法连接本地客户端，请检查启动窗口。"));
