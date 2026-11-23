// Embedded algorithm demos for the course notes. No network dependencies.
(() => {
  "use strict";

  const bootKey = Symbol.for("infinitepwn.algorithmDemo");
  if (window[bootKey]) {
    window[bootKey]();
    return;
  }

  const algorithms = Object.create(null);

  (function registerQuickselect() {
    "use strict";

    const MAX_LENGTH = 14;
    const MAX_VALUE = 9999;
    const roleInfo = {
      less: { label: "小于枢轴", className: "selected" },
      equal: { label: "等于枢轴", className: "accent" },
      pending: { label: "待检查", className: "" },
      greater: { label: "大于枢轴", className: "done" },
      outside: { label: "已排除", className: "muted" }
    };

    function readInput(values) {
      const input = String(values.array ?? "").trim().replace(/，/g, ",");
      if (!input) {
        throw new Error("至少输入 1 个整数");
      }
      const parts = input.includes(",") ? input.split(",").map(part => part.trim()) : input.split(/\s+/);
      if (parts.length > MAX_LENGTH) {
        throw new Error("数组最多支持 14 个数");
      }
      if (parts.some(part => !/^[+-]?\d+$/.test(part))) {
        throw new Error("请输入整数，用逗号或空格分隔，分隔符之间要有值");
      }
      const array = parts.map(Number);
      if (array.some(value => !Number.isSafeInteger(value) || Math.abs(value) > MAX_VALUE)) {
        throw new Error("每个整数须在 −9999 到 9999 之间");
      }

      const rankText = String(values.k ?? "").trim();
      const rank = Number(rankText);
      if (!/^\d+$/.test(rankText) || !Number.isSafeInteger(rank) || rank < 1 || rank > array.length) {
        throw new Error("目标秩 k 须是 1 到 " + array.length + " 之间的整数");
      }
      return { array, rank };
    }

    function swap(array, left, right) {
      [array[left], array[right]] = [array[right], array[left]];
    }

    function build(values) {
      const { array, rank } = readInput(values);
      const frames = [];
      let l = 0;
      let r = array.length;
      let k = rank;

      while (l < r) {
        const pivot = array[l];
        let lt = l;
        let i = l;
        let gt = r;

        function record(title, detail, extra = {}) {
          frames.push({ array: array.slice(), title, detail, l, r, k, pivot, lt, i, gt, ...extra });
        }

        if (r - l === 1) {
          lt = l;
          i = gt = r;
          record("只剩一个元素", "当前目标为第 1 小，返回 " + pivot, { answer: l });
          break;
        }

        record("选择本轮枢轴", "取区间首元素 " + pivot + "，把当前区间按与枢轴的大小关系划分");
        while (i < gt) {
          const index = i;
          const value = array[i];
          if (value < pivot) {
            const destination = lt;
            swap(array, lt, i);
            lt += 1;
            i += 1;
            record(value + " 小于枢轴", "把 A[" + index + "] 放进左段的下标 " + destination + "，lt 和 i 各右移一格");
          } else if (value > pivot) {
            gt -= 1;
            swap(array, i, gt);
            const note = i < gt ? "，交换回来的 " + array[i] + " 待检查，i 留在原处" : "，待检查段已空";
            record(value + " 大于枢轴", "gt 左移一格，把 A[" + index + "] 放进右段的下标 " + gt + note);
          } else {
            i += 1;
            record(value + " 等于枢轴", "把 A[" + index + "] 纳入等值段，i 右移一格");
          }
        }

        const smaller = lt - l;
        const equal = gt - lt;
        const leftAndEqual = smaller + equal;
        if (k <= smaller) {
          record("进入左段，目标秩不变", "左段占当前秩 1–" + smaller + "，在这一段继续找第 " + k + " 小", { retain: "less" });
          r = lt;
        } else if (k <= leftAndEqual) {
          const equalRanks = equal === 1 ? "第 " + leftAndEqual + " 小" : "第 " + (smaller + 1) + " 至第 " + leftAndEqual + " 小";
          record("目标落在等值段", equalRanks + "都等于 " + pivot + "，返回 " + pivot, { answer: l + k - 1 });
          break;
        } else {
          const nextRank = k - leftAndEqual;
          record("进入右段，重新计算目标秩", "去掉排在右段前面的 " + smaller + " 个较小值和 " + equal + " 个等值，新秩为 " + k + " − " + smaller + " − " + equal + " = " + nextRank, { retain: "greater" });
          k = nextRank;
          l = gt;
        }
      }
      return frames;
    }

    function element(tag, className, content) {
      const node = document.createElement(tag);
      node.className = className;
      if (content !== undefined) {
        node.textContent = content;
      }
      return node;
    }

    function roleAt(frame, index) {
      if (index < frame.l || index >= frame.r) return "outside";
      if (index < frame.lt) return "less";
      if (index < frame.i) return "equal";
      if (index < frame.gt) return "pending";
      return "greater";
    }

    const styles = [
        ".qs-board{display:grid;gap:.75rem;min-width:0}",
        ".qs-board .qs-row{display:flex;flex-wrap:wrap;gap:.42rem;align-items:flex-start}",
        ".qs-cell{display:grid;justify-items:center;gap:.16rem}",
        ".qs-board .qs-cell .tile{width:auto;min-width:2.2rem;height:auto;min-height:2.2rem;padding:.18rem .37rem;display:grid;place-items:center}",
        ".qs-cell .qs-index{font-size:.66rem;line-height:1.1;opacity:.65}",
        ".qs-board .qs-legend{display:flex;flex-wrap:wrap;gap:.4rem .85rem}",
        ".qs-board .qs-key{display:inline-flex;align-items:center;gap:.35rem;white-space:nowrap}",
        ".qs-board .qs-swatch.tile{width:.7rem;height:.7rem;min-width:0;min-height:0;padding:0;flex:none}",
        ".qs-board .qs-keep .tile{box-shadow:inset 0 -3px currentColor}",
        ".qs-board .qs-answer.tile{outline:2px solid currentColor;outline-offset:2px}"
    ].join("\n");

    function render(stage, frame) {
      const board = element("div", "qs-board");
      const meta = element("div", "viz-meta");
      [
        "当前区间 A[" + frame.l + "…" + (frame.r - 1) + "]",
        "枢轴 " + frame.pivot,
        "当前找第 " + frame.k + " 小"
      ].forEach(label => meta.append(element("span", "", label)));
      board.append(meta);

      const row = element("div", "viz-row qs-row");
      row.setAttribute("aria-label", "数组，下标从 0 开始");
      row.setAttribute("role", "list");
      const counts = { less: 0, equal: 0, pending: 0, greater: 0 };
      frame.array.forEach((value, index) => {
        const role = roleAt(frame, index);
        const info = roleInfo[role];
        const active = role === "pending" && index === frame.i;
        const answer = index === frame.answer;
        const retain = role === frame.retain;
        const cell = element("div", "qs-cell" + (retain ? " qs-keep" : ""));
        const tile = element("span", ["tile", info.className, active ? "current" : "", answer ? "qs-answer" : ""].filter(Boolean).join(" "), value);
        const description = "下标 " + index + "，" + value + "，" + info.label + (answer ? "，返回值" : active ? "，下一次检查" : retain ? "，进入下轮" : "");
        cell.setAttribute("role", "listitem");
        cell.setAttribute("aria-label", description);
        tile.title = description;
        tile.setAttribute("aria-hidden", "true");
        const indexLabel = element("span", "mono qs-index", index);
        indexLabel.setAttribute("aria-hidden", "true");
        cell.append(tile, indexLabel);
        row.append(cell);
        if (role !== "outside") counts[role] += 1;
      });
      board.append(row);

      const legend = element("div", "legend small qs-legend");
      Object.entries(counts).forEach(([role, count]) => {
        const info = roleInfo[role];
        const key = element("span", "qs-key");
        const swatch = element("span", "tile qs-swatch " + info.className);
        swatch.setAttribute("aria-hidden", "true");
        key.append(swatch, element("span", "", info.label + " " + count));
        legend.append(key);
      });
      board.append(legend);

      if (frame.retain) {
        board.append(element("div", "viz-label small", frame.retain === "less" ? "下轮保留左段" : "下轮保留右段"));
      } else if (frame.answer !== undefined) {
        board.append(element("div", "viz-label", "返回 " + frame.array[frame.answer]));
      } else if (frame.i < frame.gt) {
        board.append(element("div", "viz-label small mono", "lt = " + frame.lt + " · i = " + frame.i + " · gt = " + frame.gt));
      }
      stage.replaceChildren(board);
    }

    algorithms.quickselect = {
      styles,
      title: "快速选择",
      fields: [
        { id: "array", label: "数组", value: "9, 2, 5, 2, 7, 2, 5, 1" },
        { id: "k", label: "目标秩 k", value: "5" }
      ],
      build,
      render
    };
  })();

  (function () {
    "use strict";


    function rangeText(task) {
      return "[" + task.start + ", " + task.finish + ")";
    }

    function shortTask(task) {
      return task.id + " " + rangeText(task);
    }

    function readTasks(raw) {
      const input = String(raw ?? "").normalize("NFKC").trim();
      if (!input) throw new Error("请输入至少一个任务区间，例如 1-4, 3-5, 4-7。");

      const parts = input
        .replace(/\[\s*(\d+)\s*,\s*(\d+)\s*\)/g, "$1-$2")
        .split(/[,;、\n]/);
      if (parts.length > 9) throw new Error("一次最多演示 9 个区间。");

      return parts.map(function (part, index) {
        const id = String.fromCharCode(65 + index);
        const bounds = part.trim().match(/^(\d{1,3})\s*(?:-|–|—|~|至)\s*(\d{1,3})$/);
        if (!bounds) throw new Error("任务 " + id + " 的格式应为 1-4 或 [1,4)，区间之间用逗号分隔。");

        const start = Number(bounds[1]);
        const finish = Number(bounds[2]);
        if (start >= finish || finish > 50) {
          throw new Error("任务 " + id + " 需满足 0 ≤ 开始时间 < 结束时间 ≤ 50。");
        }
        return { id, start, finish, index };
      });
    }

    function getScale(tasks) {
      const max = Math.max(...tasks.map(function (task) { return task.finish; }));
      const step = max <= 5 ? 1 : max <= 12 ? 2 : max <= 25 ? 5 : 10;
      return { step, end: Math.ceil(max / step) * step };
    }

    function build(values) {
      const tasks = readTasks(values.intervals);
      const sorted = tasks.slice().sort(function (a, b) {
        return a.finish - b.finish || a.index - b.index;
      });
      const selected = [];
      const skipped = [];
      const scale = getScale(tasks);

      function frame(title, detail, order, options) {
        return {
          title,
          detail,
          order,
          scale,
          selected: selected.slice(),
          skipped: skipped.slice(),
          ...options
        };
      }

      const frames = [
        frame(
          "按输入顺序编号",
          "每项任务占用 [开始, 结束)。结束时刻可以立即交给下一项任务。",
          tasks,
          { orderLabel: "输入顺序" }
        ),
        frame(
          "按结束时间从早到晚排列",
          "每次先考虑结束最早的任务。结束时间相同的任务按输入顺序排列。",
          sorted,
          { orderLabel: "结束时间顺序" }
        )
      ];

      sorted.forEach(function (task) {
        const previous = selected[selected.length - 1] || null;
        const accepted = previous === null || task.start >= previous.finish;
        let detail;

        if (!previous) {
          detail = "当前没有已选任务，先安排 " + shortTask(task) + "。";
        } else if (accepted && task.start === previous.finish) {
          detail = task.id + " 在 " + task.start + " 开始，正好接在 " + previous.id +
            " 结束后。半开区间的结束端不占用时刻 " + task.start + "，两项任务都可以安排。";
        } else if (accepted) {
          detail = task.id + " 在 " + task.start + " 开始，晚于 " + previous.id +
            " 的结束时间 " + previous.finish + "，可以安排。";
        } else {
          const start = Math.max(task.start, previous.start);
          detail = task.id + " 的开始时间 " + task.start + " 早于 " + previous.id +
            " 的结束时间 " + previous.finish + "，两项任务在 [" + start + ", " +
            previous.finish + ") 重叠，跳过 " + task.id + "。";
        }

        (accepted ? selected : skipped).push(task);
        frames.push(frame(
          "检查任务 " + task.id + " · " + (accepted ? "选入" : "跳过"),
          detail,
          sorted,
          { orderLabel: "结束时间顺序", active: task, previous, accepted }
        ));
      });

      frames.push(frame(
        "得到最多可安排的 " + selected.length + " 项任务",
        "按实际安排顺序为 " + selected.map(shortTask).join(" → ") +
          "。每次先选结束最早的相容任务，可以给后续任务留出最多的时间。",
        sorted,
        { orderLabel: "结束时间顺序", final: true }
      ));
      return frames;
    }

    function make(doc, tag, className, content) {
      const element = doc.createElement(tag);
      if (className) element.className = className;
      if (content !== undefined) element.textContent = content;
      return element;
    }

    const styles = `
  .interval-viz {
    --iv-id-col: 5.8rem;
    --iv-state-col: 3.8rem;
    --iv-gap: .75rem;
    --iv-good: var(--accent, #006961);
    --iv-base: var(--muted, #53676f);
    --iv-bad: var(--danger);
    color: var(--ink, #172e34);
    min-width: 0;
  }
  .interval-viz .iv-legend {
    display: flex; align-items: center; flex-wrap: wrap; gap: .35rem .95rem;
    color: var(--muted, #53676f); font-size: .78rem; margin-bottom: 1rem;
  }
  .interval-viz .iv-legend-symbol {
    display: inline-block; width: .55rem; height: .55rem; margin: 0 .3rem .02rem 0;
    border: 1px solid var(--iv-base); border-radius: 50%; vertical-align: baseline;
  }
  .interval-viz .iv-legend-symbol.start { background: var(--iv-base); }
  .interval-viz .iv-legend-symbol.end { background: var(--surface, #fff); }
  .interval-viz .iv-legend-limit { color: var(--iv-good); }
  .interval-viz .iv-grid {
    display: grid; grid-template-columns: var(--iv-id-col) minmax(0, 1fr) var(--iv-state-col);
    column-gap: var(--iv-gap); align-items: center;
  }
  .interval-viz .iv-axis {
    color: var(--muted, #53676f); font-size: .75rem; margin-bottom: .35rem;
  }
  .interval-viz .iv-axis-track { position: relative; height: 1.6rem; }
  .interval-viz .iv-tick-label {
    position: absolute; top: .25rem; transform: translateX(-50%);
    font-variant-numeric: tabular-nums; line-height: 1; white-space: nowrap;
  }
  .interval-viz .iv-tick-label.first { transform: none; }
  .interval-viz .iv-tick-label.last { transform: translateX(-100%); }
  .interval-viz .iv-row {
    min-height: 2.4rem; border-top: 1px solid var(--line, #dfe8e8);
    color: var(--muted, #53676f);
  }
  .interval-viz .iv-row:last-of-type { border-bottom: 1px solid var(--line, #dfe8e8); }
  .interval-viz .iv-row.is-active {
    background: var(--soft, #e9f4f1);
    border-radius: .35rem;
  }
  .interval-viz .iv-label {
    display: flex; gap: .42rem; align-items: baseline; min-width: 0;
    padding-left: .2rem; font-size: .78rem; white-space: nowrap;
    font-variant-numeric: tabular-nums;
  }
  .interval-viz .iv-label strong { color: var(--ink, #172e34); }
  .interval-viz .iv-track { position: relative; align-self: stretch; min-height: 2.25rem; }
  .interval-viz .iv-guide {
    position: absolute; display: block; inset-block: 0; width: 1px;
    background: var(--line, #dfe8e8); pointer-events: none;
  }
  .interval-viz .iv-guide.limit {
    width: 0; border-left: 1px dashed var(--iv-good); background: transparent;
  }
  .interval-viz .iv-bar {
    position: absolute; height: .22rem; top: calc(50% - .11rem);
    background: currentColor; border-radius: 999px; min-width: 1px; z-index: 1;
  }
  .interval-viz .iv-row.is-selected { color: var(--iv-good); }
  .interval-viz .iv-row.is-skipped { color: var(--iv-base); }
  .interval-viz .iv-row.is-skipped .iv-bar { opacity: .5; }
  .interval-viz .iv-row.is-active.is-skipped { color: var(--iv-bad); }
  .interval-viz .iv-row.is-active.is-skipped .iv-bar { opacity: 1; }
  .interval-viz .iv-bar::before,
  .interval-viz .iv-bar::after {
    content: ""; position: absolute; top: 50%; width: .5rem; height: .5rem;
    box-sizing: border-box; border: 1.5px solid currentColor; border-radius: 50%;
  }
  .interval-viz .iv-bar::before {
    left: 0; background: currentColor; transform: translate(-50%, -50%);
  }
  .interval-viz .iv-bar::after {
    right: 0; background: var(--surface, #fff); transform: translate(50%, -50%);
  }
  .interval-viz .iv-overlap {
    position: absolute; top: calc(50% - .42rem); height: .84rem; z-index: 0;
    border-radius: .22rem; background: color-mix(in srgb, var(--iv-bad) 18%, transparent);
  }
  .interval-viz .iv-status {
    font-size: .74rem; white-space: nowrap; text-align: center; font-weight: 500;
  }
  .interval-viz .iv-result {
    display: flex; flex-wrap: wrap; align-items: center; gap: .45rem;
    margin-top: .9rem; color: var(--muted, #53676f); font-size: .82rem;
  }
  .interval-viz .iv-result-task {
    display: inline-block; padding: .16rem .42rem; border-radius: .25rem;
    background: var(--soft, #e9f4f1); color: var(--iv-good); white-space: nowrap;
    font-variant-numeric: tabular-nums;
  }
  @container algorithm-card (inline-size <= 520px) {
    .interval-viz { --iv-id-col: 3.05rem; --iv-state-col: 2.7rem; --iv-gap: .35rem; }
    .interval-viz .iv-label { display: grid; gap: 0; padding-left: 0; font-size: .68rem; }
    .interval-viz .iv-axis, .interval-viz .iv-status { font-size: .68rem; }
    .interval-viz .iv-row { min-height: 2.2rem; }
  }
  `;

    function render(stage, frame) {
      const doc = stage.ownerDocument;
      const plot = make(doc, "div", "interval-viz");
      const legend = make(doc, "div", "iv-legend");
      [["start", "开始时刻"], ["end", "结束时刻"]].forEach(function (item) {
        const entry = make(doc, "span");
        const symbol = make(doc, "span", "iv-legend-symbol " + item[0]);
        symbol.setAttribute("aria-hidden", "true");
        entry.append(symbol, item[1]);
        legend.appendChild(entry);
      });

      if (frame.previous) {
        legend.appendChild(make(
          doc, "span", "iv-legend-limit",
          "虚线：上一项 " + frame.previous.id + " 在 " + frame.previous.finish + " 结束"
        ));
      }
      plot.appendChild(legend);

      const ticks = [];
      for (let time = 0; time <= frame.scale.end; time += frame.scale.step) ticks.push(time);
      function percent(time) {
        return (time * 100 / frame.scale.end) + "%";
      }

      const axis = make(doc, "div", "iv-grid iv-axis");
      const axisTrack = make(doc, "div", "iv-axis-track");
      ticks.forEach(function (time, index) {
        const position = index === 0 ? " first" : index === ticks.length - 1 ? " last" : "";
        const tick = make(doc, "span", "iv-tick-label" + position, String(time));
        tick.style.left = percent(time);
        axisTrack.appendChild(tick);
      });
      axisTrack.setAttribute("aria-hidden", "true");
      axis.append(
        make(doc, "span", "", frame.orderLabel),
        axisTrack,
        make(doc, "span", "iv-status", "状态")
      );
      plot.appendChild(axis);

      const selected = new Set(frame.selected.map(function (task) { return task.id; }));
      const skipped = new Set(frame.skipped.map(function (task) { return task.id; }));
      const rows = make(doc, "div");
      rows.setAttribute("role", "list");
      rows.setAttribute("aria-label", frame.orderLabel + "的任务区间");

      frame.order.forEach(function (task) {
        const active = frame.active?.id === task.id;
        const chosen = selected.has(task.id);
        const rejected = skipped.has(task.id);
        const status = chosen ? "已选" : rejected ? "跳过" : "待比较";
        const state = chosen ? " is-selected" : rejected ? " is-skipped" : "";
        const row = make(doc, "div", "iv-row iv-grid" + state + (active ? " is-active" : ""));
        row.setAttribute("role", "listitem");
        if (active) row.setAttribute("aria-current", "step");

        const label = make(doc, "span", "iv-label");
        label.append(make(doc, "strong", "", task.id), make(doc, "span", "", rangeText(task)));

        const track = make(doc, "div", "iv-track");
        track.setAttribute("aria-hidden", "true");
        ticks.forEach(function (time) {
          const guide = make(doc, "span", "iv-guide");
          guide.style.left = percent(time);
          track.appendChild(guide);
        });
        if (frame.previous) {
          const limit = make(doc, "span", "iv-guide limit");
          limit.style.left = percent(frame.previous.finish);
          track.appendChild(limit);
        }

        if (active && !frame.accepted && frame.previous) {
          const overlapStart = Math.max(task.start, frame.previous.start);
          const overlap = make(doc, "span", "iv-overlap");
          overlap.style.left = percent(overlapStart);
          overlap.style.width = percent(frame.previous.finish - overlapStart);
          track.appendChild(overlap);
        }

        const bar = make(doc, "span", "iv-bar");
        bar.style.left = percent(task.start);
        bar.style.width = percent(task.finish - task.start);
        track.appendChild(bar);

        row.append(label, track, make(doc, "span", "iv-status", status));
        rows.appendChild(row);
      });
      plot.appendChild(rows);

      if (frame.final) {
        const result = make(doc, "div", "iv-result");
        result.appendChild(make(doc, "span", "", "安排顺序"));
        frame.selected.forEach(function (task) {
          result.appendChild(make(doc, "span", "iv-result-task", shortTask(task)));
        });
        plot.appendChild(result);
      }

      stage.replaceChildren(plot);
    }

    algorithms.interval = {
      styles,
      title: "区间调度",
      fields: [{ id: "intervals", label: "任务区间", value: "1-4, 3-5, 0-6, 4-7, 8-11" }],
      build,
      render
    };
  }());

  (() => {
    const fields = [
      { id: "x", label: "字符串 X", value: "ABCBDAB" },
      { id: "y", label: "字符串 Y", value: "BDCABA" },
    ];
    const limit = 9;
    const arrows = { diagonal: "↖", up: "↑", left: "←" };

    function glyph(symbol) {
      return { " ": "␠", "\t": "⇥", "\n": "↵", "\r": "␍" }[symbol] ?? symbol;
    }

    function cell(i, j) {
      return `L(${i}, ${j})`;
    }

    function build(values = {}) {
      const x = Array.from(String(values.x ?? fields[0].value));
      const y = Array.from(String(values.y ?? fields[1].value));
      if (x.length > limit || y.length > limit) throw new Error("每个字符串最多输入 9 个字符。");
      const dp = Array.from({ length: x.length + 1 }, (_, i) =>
        Array.from({ length: y.length + 1 }, (_, j) => i === 0 || j === 0 ? 0 : null)
      );
      const directions = dp.map((row) => row.map(() => null));
      const frames = [];

      function addFrame(frame) {
        frames.push({ x, y, table: dp.map((row) => row.slice()), ...frame });
      }

      addFrame({
        phase: "initialize",
        title: "初始化空前缀",
        detail: "L(i, j) 表示 X 前 i 个字符与 Y 前 j 个字符的最长公共子序列长度。只要一边为空，长度就是 0。",
      });

      for (let i = 1; i <= x.length; i += 1) {
        for (let j = 1; j <= y.length; j += 1) {
          const charX = glyph(x[i - 1]);
          const charY = glyph(y[j - 1]);
          const up = { i: i - 1, j };
          const left = { i, j: j - 1 };
          const diagonal = { i: i - 1, j: j - 1 };
          let dependencies;
          let detail;

          if (x[i - 1] === y[j - 1]) {
            const previous = dp[i - 1][j - 1];
            dp[i][j] = previous + 1;
            directions[i][j] = "diagonal";
            dependencies = [diagonal];
            detail = `两个末尾字符都是「${charX}」。把它接在较短前缀的解后面，${cell(i, j)} = ${cell(i - 1, j - 1)} + 1 = ${previous} + 1 = ${dp[i][j]}。`;
          } else {
            const upValue = dp[i - 1][j];
            const leftValue = dp[i][j - 1];
            dp[i][j] = Math.max(upValue, leftValue);
            directions[i][j] = upValue >= leftValue ? "up" : "left";
            dependencies = [up, left];
            detail = `末尾「${charX}」和「${charY}」无法配对。去掉 X 末尾得到上方的 ${upValue}，去掉 Y 末尾得到左方的 ${leftValue}，本格取最大值 ${dp[i][j]}。`;
            if (upValue === leftValue) {
              detail += "两格相同，回溯时固定向上。";
            }
          }

          addFrame({
            phase: "fill",
            title: `计算 ${cell(i, j)}`,
            detail,
            current: { i, j },
            direction: directions[i][j],
            dependencies,
          });
        }
      }

      let i = x.length;
      let j = y.length;
      const length = dp[i][j];
      const route = [{ i, j }];
      const matches = [];
      const recovered = [];

      if (i > 0 && j > 0) {
        addFrame({
          phase: "trace",
          title: "从右下角回溯",
          detail: `${cell(i, j)} 给出最优长度 ${length}。沿填表时记录的方向回到空前缀，遇到对角箭头就收下当前匹配的字符。`,
          current: { i, j },
          route: route.slice(),
          matches: [],
          symbols: [],
          subsequence: "",
        });
      }

      while (i > 0 && j > 0) {
        const from = { i, j };
        const direction = directions[i][j];
        let title;
        let detail;

        if (direction === "diagonal") {
          const symbol = x[i - 1];
          const char = glyph(symbol);
          matches.push(from);
          recovered.unshift(symbol);
          i -= 1;
          j -= 1;
          title = `收下匹配字符「${char}」`;
          detail = `两个末尾字符匹配，由 ${cell(from.i, from.j)} 向左上回到 ${cell(i, j)}。回溯先找到靠后的字符，因此把「${char}」加到当前结果的开头。`;
        } else {
          const upward = direction === "up";
          const discarded = glyph(upward ? x[i - 1] : y[j - 1]);
          const tie = dp[i - 1][j] === dp[i][j - 1];
          if (upward) {
            i -= 1;
          } else {
            j -= 1;
          }
          title = `跳过 ${upward ? "X" : "Y"} 的「${discarded}」`;
          detail = `向${upward ? "上" : "左"}回到 ${cell(i, j)}，最优长度仍为 ${dp[i][j]}。`;
          if (tie) {
            detail += "两个方向都能得到最优解，这里按规则向上。";
          }
        }

        const current = { i, j };
        route.push(current);
        addFrame({
          phase: "trace",
          title,
          detail,
          current,
          from,
          direction,
          route: route.slice(),
          matches: matches.slice(),
          symbols: recovered.slice(),
          subsequence: recovered.join(""),
        });
      }

      const subsequence = recovered.join("");
      const readable = recovered.map(glyph).join("");
      let detail;
      if (length > 0) {
        detail = `「${readable}」按原顺序出现在 X 和 Y 中，长度为 ${length}。`;
      } else if (x.length === 0 || y.length === 0) {
        detail = "至少有一个输入为空，最长公共子序列为空，长度为 0。";
      } else {
        detail = "两串没有可配对的字符，最长公共子序列为空，长度为 0。";
      }
      addFrame({
        phase: "done",
        title: "得到一个最长公共子序列",
        detail,
        route: route.slice(),
        matches: matches.slice(),
        symbols: recovered.slice(),
        subsequence,
        length,
      });

      return frames;
    }

    const styles = `
      .lcs-viz {
        color: var(--ink, #202c2a);
        min-width: 0;
        max-width: 100%;
        display: grid;
        gap: .9rem;
      }
      .lcs-viz .lcs-scroll {
        min-width: 0;
        max-width: 100%;
        overflow-x: auto;
        overscroll-behavior-x: contain;
        border-radius: .65rem;
        padding: .2rem .15rem .45rem;
      }
      .lcs-viz .lcs-scroll:focus-visible {
        outline: 2px solid var(--accent, #346659);
        outline-offset: -2px;
      }
      .lcs-viz .lcs-table {
        width: max-content;
        margin: 0 auto;
        border-spacing: 3px;
        border-collapse: separate;
        font: inherit;
        text-align: center;
      }
      .lcs-viz .lcs-table th,
      .lcs-viz .lcs-table td {
        min-width: 2.55rem;
        height: 2.55rem;
        padding: .1rem .25rem;
        border: 1px solid var(--line, #dddcd3);
        border-radius: .3rem;
        text-align: center;
        vertical-align: middle;
        white-space: pre;
      }
      .lcs-viz .lcs-table th {
        background: var(--surface, #f0eee8);
        line-height: 1.1;
      }
      .lcs-viz .lcs-table .lcs-corner {
        font-size: .72rem;
        line-height: 1.15;
        white-space: normal;
      }
      .lcs-viz .lcs-index {
        display: block;
        color: var(--muted, #64706a);
        font-size: .66rem;
        font-weight: 500;
      }
      .lcs-viz .lcs-table td {
        background: var(--paper, #fff);
        font-variant-numeric: tabular-nums;
      }
      .lcs-viz .lcs-table .lcs-empty {
        color: var(--muted, #64706a);
        background: var(--surface, #f0eee8);
      }
      .lcs-viz .lcs-table .lcs-dependency,
      .lcs-viz .lcs-legend .lcs-dependency {
        background: var(--soft, #e4ede5);
        border-color: var(--accent, #346659);
        border-style: dashed;
      }
      .lcs-viz .lcs-table .lcs-route,
      .lcs-viz .lcs-legend .lcs-route {
        background: var(--soft, #e4ede5);
        border-color: var(--accent, #346659);
      }
      .lcs-viz .lcs-table .lcs-match,
      .lcs-viz .lcs-legend .lcs-match {
        background: var(--accent, #346659);
        color: var(--accent-ink, #fff);
        border-color: var(--accent, #346659);
      }
      .lcs-viz .lcs-table .lcs-current,
      .lcs-viz .lcs-legend .lcs-current {
        border-color: var(--accent, #346659);
        box-shadow: inset 0 0 0 1px var(--accent, #346659);
        font-weight: 750;
      }
      .lcs-viz .lcs-direction {
        margin-left: .22rem;
        font-size: .75em;
      }
      .lcs-viz .lcs-legend {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: .35rem .85rem;
        color: var(--muted, #64706a);
        font-size: .78rem;
      }
      .lcs-viz .lcs-key {
        display: inline-flex;
        align-items: center;
        gap: .3rem;
      }
      .lcs-viz .lcs-chip {
        width: .7rem;
        height: .7rem;
        border-radius: .15rem;
        border: 1px solid var(--line, #dddcd3);
      }
      .lcs-viz .lcs-recovered {
        display: flex;
        align-items: baseline;
        justify-content: center;
        flex-wrap: wrap;
        gap: .35rem .65rem;
        font-size: .9rem;
      }
      .lcs-viz .lcs-recovered strong {
        max-width: 100%;
        overflow-wrap: anywhere;
        white-space: pre-wrap;
        color: var(--accent, #346659);
        font-weight: 750;
        letter-spacing: .055em;
      }
      .lcs-viz .lcs-length {
        color: var(--muted, #64706a);
      }
      @container algorithm-card (inline-size <= 520px) {
        .lcs-viz .lcs-table th,
        .lcs-viz .lcs-table td {
          min-width: 2.15rem;
          height: 2.15rem;
        }
      }
    `;

    function render(stage, frame) {
      const doc = stage.ownerDocument;

      function make(tag, className, value) {
        const el = doc.createElement(tag);
        if (className) el.className = className;
        if (value !== undefined) el.textContent = value;
        return el;
      }

      function heading(axis, index, symbol) {
        const header = make("th", "", symbol === undefined ? "∅" : glyph(symbol));
        header.scope = axis === "X" ? "row" : "col";
        header.append(make("span", "lcs-index", index));
        header.setAttribute("aria-label", index === 0 ? `空的 ${axis} 前缀` : `${axis} 第 ${index} 字符 ${glyph(symbol)}`);
        return header;
      }

      function matchesCell(position, i, j) {
        return position?.i === i && position?.j === j;
      }

      const oldScroll = stage.querySelector(".lcs-scroll")?.scrollLeft ?? 0;
      const visual = make("div", "lcs-viz");
      const scroller = make("div", "lcs-scroll");
      scroller.tabIndex = 0;
      scroller.setAttribute("role", "region");
      scroller.setAttribute("aria-label", "最长公共子序列表格");
      const table = make("table", "lcs-table");
      table.setAttribute("aria-label", "X 前缀对应行，Y 前缀对应列");
      const thead = make("thead");
      const top = make("tr");
      const corner = make("th", "lcs-corner", "X ↓ Y →");
      top.append(corner, heading("Y", 0));
      frame.y.forEach((symbol, index) => top.append(heading("Y", index + 1, symbol)));
      thead.append(top);
      table.append(thead);

      let activeCell;
      const tbody = make("tbody");
      frame.table.forEach((values, i) => {
        const row = make("tr");
        row.append(heading("X", i, frame.x[i - 1]));
        values.forEach((value, j) => {
          const entry = make("td", value === null ? "lcs-empty" : "", value ?? "·");
          if (value === null) entry.setAttribute("aria-label", "未计算");
          if (frame.dependencies?.some((item) => matchesCell(item, i, j))) {
            entry.classList.add("lcs-dependency");
          }
          if (frame.route?.some((item) => matchesCell(item, i, j))) {
            entry.classList.add("lcs-route");
          }
          if (frame.matches?.some((item) => matchesCell(item, i, j))) {
            entry.classList.add("lcs-match");
          }
          const isCurrent = matchesCell(frame.current, i, j);
          if (isCurrent) {
            entry.classList.add("lcs-current");
            activeCell = entry;
          }
          const showArrow = frame.phase === "fill" ? isCurrent : matchesCell(frame.from, i, j);
          if (showArrow && frame.direction) {
            const arrow = make("span", "lcs-direction", arrows[frame.direction]);
            arrow.setAttribute("aria-hidden", "true");
            entry.append(arrow);
          }
          row.append(entry);
        });
        tbody.append(row);
      });
      table.append(tbody);
      scroller.append(table);
      visual.append(scroller);

      const keys = [];
      if (frame.current) keys.push(["lcs-current", "当前状态"]);
      if (frame.dependencies?.length) keys.push(["lcs-dependency", "本次依赖"]);
      if (frame.route?.length) keys.push(["lcs-route", "回溯路径"]);
      if (frame.matches?.length) keys.push(["lcs-match", "收下字符"]);
      if (keys.length) {
        const legend = make("div", "lcs-legend");
        for (const [kind, label] of keys) {
          const key = make("span", "lcs-key");
          const chip = make("span", `lcs-chip ${kind}`);
          chip.setAttribute("aria-hidden", "true");
          key.append(chip, make("span", "", label));
          legend.append(key);
        }
        visual.append(legend);
      }

      if (frame.phase === "trace" || frame.phase === "done") {
        const done = frame.phase === "done";
        const result = make("div", "lcs-recovered");
        const recovered = frame.symbols.map(glyph).join("");
        result.append(make("span", "", done ? "公共子序列" : "已收下的字符"));
        result.append(make("strong", "", recovered || (done ? "空序列" : "暂为空")));
        if (done) result.append(make("span", "lcs-length", `长度 ${frame.length}`));
        visual.append(result);
      }

      stage.replaceChildren(visual);
      scroller.scrollLeft = oldScroll;
      if (activeCell) {
        const visible = scroller.getBoundingClientRect();
        const target = activeCell.getBoundingClientRect();
        if (target.right > visible.right) {
          scroller.scrollLeft += target.right - visible.right + 4;
        } else if (target.left < visible.left) {
          scroller.scrollLeft -= visible.left - target.left + 4;
        }
      }
    }

    algorithms.lcs = {
      styles,
      title: "最长公共子序列",
      fields,
      build,
      render,
    };
  })();

  const cardStyles = `
:host {
  display: block;
  min-inline-size: 0;
  max-inline-size: 100%;
  margin-block: 1.2rem 1.5rem;
  container: algorithm-card / inline-size;
  color-scheme: light;
  --ink: #1b3027;
  --muted: #4e645a;
  --accent: #245e46;
  --accent-ink: #fffef9;
  --soft: #e9f0e9;
  --line: #ccd8cf;
  --paper: #f5f6f1;
  --surface: #fdfefb;
  --focus: #307754;
  --danger: #9b342e;
  --partition-right: #dce8f0;
  --partition-right-ink: #2b4c60;
  --mono: ui-monospace, SFMono-Regular, Consolas, monospace;
  color: var(--ink);
  font: 0.9rem/1.55 system-ui, -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
}

:host([hidden]) { display: none; }

:host([data-demo-theme="dark"]) {
  color-scheme: dark;
  --ink: #e5efe7;
  --muted: #acbfb3;
  --accent: #a6d9b7;
  --accent-ink: #13271b;
  --soft: #2a3e32;
  --line: #42574b;
  --paper: #1b2821;
  --surface: #202f27;
  --focus: #b1e3c1;
  --danger: #f4a69f;
  --partition-right: #304650;
  --partition-right-ink: #d9ecf1;
}

@media (prefers-color-scheme: dark) {
  :host(:not([data-demo-theme])) {
    color-scheme: dark;
    --ink: #e5efe7;
    --muted: #acbfb3;
    --accent: #a6d9b7;
    --accent-ink: #13271b;
    --soft: #2a3e32;
    --line: #42574b;
    --paper: #1b2821;
    --surface: #202f27;
    --focus: #b1e3c1;
    --danger: #f4a69f;
  --partition-right: #304650;
  --partition-right-ink: #d9ecf1;
  }
}

*, *::before, *::after { box-sizing: border-box; }
button, input { font: inherit; }
button, input[type="range"] { cursor: pointer; }
button:disabled, input:disabled { cursor: default; }
button:focus-visible, input:focus-visible, a:focus-visible, [tabindex]:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 3px;
}
a { color: var(--accent); text-underline-offset: .2em; }

.panel {
  min-inline-size: 0;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: var(--surface);
}

.workbench { display: grid; grid-template-columns: minmax(0, 1fr); }
.setup, .viewer { min-inline-size: 0; padding: 13px 16px; }
.setup { border-block-end: 1px solid var(--line); }
.setup form, #fields { display: grid; min-inline-size: 0; gap: 9px; }
.field { display: grid; min-inline-size: 0; gap: 4px; }
.field > span { color: var(--muted); font-size: .83rem; font-weight: 670; }
.field input {
  inline-size: 100%;
  min-inline-size: 0;
  min-block-size: 40px;
  padding: 5px 9px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--paper);
  color: var(--ink);
  font-size: 1rem;
}
.field input[aria-invalid="true"] { border-color: var(--danger); }
.field .hint, .hint {
  margin: 0;
  color: var(--muted);
  font-size: .77rem;
  font-weight: 400;
  line-height: 1.4;
}
.apply, .transport button {
  min-block-size: 39px;
  padding: 5px 10px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--surface);
  color: var(--ink);
  font-size: .85rem;
  font-weight: 670;
  line-height: 1.3;
}
.apply, #play, .transport button[data-action="play"] {
  border-color: var(--accent);
  background: var(--accent);
  color: var(--accent-ink);
}
.apply { justify-self: start; }
.apply:hover, #play:hover:not(:disabled), .transport button[data-action="play"]:hover:not(:disabled) { filter: brightness(.9); }
.transport button:not(#play):not([data-action="play"]):hover:not(:disabled) {
  border-color: var(--accent);
  background: var(--soft);
}
.transport button:disabled { opacity: .5; }
#error { margin: 0; color: var(--danger); font-size: .82rem; overflow-wrap: anywhere; }
#error:empty { display: none; }

.stage-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 2px 12px;
  margin-block-end: 7px;
}
.stage-head strong { font-weight: 740; }
#count, .step-count { color: var(--accent); font-size: .81rem; font-weight: 690; font-variant-numeric: tabular-nums; }
#stage {
  min-inline-size: 0;
  min-block-size: 7.5rem;
  padding: 12px;
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
}
.viz-row { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
.mono, .tile { font-family: var(--mono); font-variant-numeric: tabular-nums; }
.tile {
  display: inline-grid;
  place-items: center;
  min-inline-size: 34px;
  min-block-size: 34px;
  padding: 3px 6px;
  border: 1px solid var(--line);
  border-radius: 5px;
  background: var(--surface);
  color: var(--ink);
  font-weight: 670;
}
.explanation { margin-block-start: 10px; }
.explanation h4 { margin: 0; font-size: .92rem; font-weight: 740; }
.explanation p { margin: 3px 0 0; color: var(--muted); overflow-wrap: anywhere; }

.transport {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 7px 11px;
  margin-block-start: 10px;
  padding-block-start: 10px;
  border-block-start: 1px solid var(--line);
}
.controls { display: flex; flex-wrap: wrap; gap: 5px; }
.progress-box {
  display: flex;
  flex: 1 1 154px;
  align-items: center;
  gap: 5px 8px;
  min-inline-size: 0;
  color: var(--muted);
  font-size: .79rem;
}
.transport input[type="range"] {
  flex: 1 1 110px;
  inline-size: 100%;
  min-inline-size: 0;
  min-block-size: 32px;
  margin: 0;
  accent-color: var(--accent);
}

@container algorithm-card (inline-size >= 620px) {
  .workbench { grid-template-columns: minmax(164px, .36fr) minmax(0, 1fr); }
  .setup { border-block-end: 0; border-inline-end: 1px solid var(--line); }
  .apply { inline-size: 100%; }
  #stage { padding: 14px; }
}

@container algorithm-card (inline-size <= 380px) {
  .setup, .viewer { padding-inline: 11px; }
  .apply, .transport button { min-block-size: 44px; }
  .controls { flex: 1 1 100%; }
  .transport button { flex: 1 1 auto; }
  .progress-box { flex-basis: 100%; }
  #stage { padding: 9px; }
}

.viz-meta { display: flex; flex-wrap: wrap; gap: 2px 12px; font-size: .81rem; font-weight: 650; }
.viz-label { color: var(--accent); font-weight: 690; }
.small { color: var(--muted); font-size: .77rem; }
.tile.selected { border-color: var(--accent); background: var(--soft); color: var(--accent); }
.tile.accent { border-color: var(--accent); background: var(--accent); color: var(--accent-ink); }
.tile.done { border-color: var(--partition-right-ink); background: var(--partition-right); color: var(--partition-right-ink); }
.tile.muted { border-style: dashed; color: var(--muted); opacity: .68; }
.tile.current { outline: 2px solid var(--focus); outline-offset: 1px; }
`;

  const selector = ".algorithm-demo[data-algorithm]";
  const instances = new Map();
  const hints = {
    quickselect: "用逗号分隔整数，k 从 1 开始。",
    interval: "写成 起点-终点，用逗号分隔任务。",
    lcs: "每个字符串最多 9 个字符，也可以留空。"
  };

  const template = document.createElement("template");
  template.innerHTML = `
    <section class="panel">
      <div class="workbench">
        <div class="setup">
          <form id="settings">
            <div id="fields"></div>
            <p class="hint" id="format"></p>
            <button class="apply" type="submit">应用输入</button>
            <p id="error" role="alert"></p>
          </form>
        </div>
        <div class="viewer">
          <div class="stage-head"><strong>执行过程</strong><span id="count"></span></div>
          <div id="stage"></div>
          <div class="explanation" aria-live="polite" aria-atomic="true">
            <h4 id="step-title"></h4><p id="detail"></p>
          </div>
          <div class="transport">
            <div class="controls">
              <button type="button" id="prev">← 上一步</button>
              <button type="button" id="play">播放</button>
              <button type="button" id="next">下一步 →</button>
            </div>
            <label class="progress-box">
              <input type="range" id="progress" min="0" value="0" aria-label="跳到指定步骤">
            </label>
          </div>
        </div>
      </div>
    </section>
  `;

  function mount(host, key) {
    const model = algorithms[key];
    const root = host.shadowRoot ?? host.attachShadow({ mode: "open" });
    const style = document.createElement("style");
    style.textContent = cardStyles + "\n" + model.styles;
    root.replaceChildren(style, template.content.cloneNode(true));

    const get = id => root.getElementById(id);
    const form = get("settings");
    const error = get("error");
    const progress = get("progress");
    const controls = {
      prev: get("prev"), play: get("play"), next: get("next")
    };
    const count = get("count");
    const stage = get("stage");
    const title = get("step-title");
    const detail = get("detail");
    const events = new AbortController();
    const eventOptions = { signal: events.signal };
    let frames;
    let index = 0;
    let timer;

    root.querySelector(".panel").setAttribute("aria-label", model.title + "交互演示");
    get("format").textContent = hints[key];
    for (const field of model.fields) {
      const label = document.createElement("label");
      label.className = "field";
      const prompt = document.createElement("span");
      prompt.textContent = field.label;
      const input = document.createElement("input");
      input.name = field.id;
      input.value = host.dataset[field.id] ?? field.value;
      input.autocomplete = "off";
      input.spellcheck = false;
      input.setAttribute("aria-describedby", "format error");
      if (field.id === "k") input.inputMode = "numeric";
      label.append(prompt, input);
      get("fields").append(label);
    }

    function stop() {
      if (timer !== undefined) window.clearInterval(timer);
      timer = undefined;
    }

    function draw() {
      const frame = frames[index];
      const last = frames.length - 1;
      if (index === last) stop();
      model.render(stage, frame);
      title.textContent = frame.title;
      detail.textContent = frame.detail;
      count.textContent = `步骤 ${index + 1} / ${frames.length}`;
      progress.max = last;
      progress.value = index;
      progress.disabled = last === 0;
      progress.setAttribute("aria-valuetext", count.textContent);
      controls.prev.disabled = index === 0;
      controls.next.disabled = index === last;
      controls.play.disabled = last === 0;
      controls.play.textContent = timer !== undefined ? "暂停" : index === last && last > 0 ? "重播" : "播放";
    }

    function applyInput() {
      try {
        frames = model.build(Object.fromEntries(new FormData(form)));
        index = 0;
        error.textContent = "";
      } catch (invalidInput) {
        error.textContent = invalidInput.message;
        if (frames === undefined) {
          const defaults = Object.fromEntries(model.fields.map(field => [field.id, field.value]));
          frames = model.build(defaults);
        }
      }
    }

    function jump(newIndex) {
      stop();
      index = Math.min(Math.max(newIndex, 0), frames.length - 1);
      draw();
    }

    form.addEventListener("submit", event => {
      event.preventDefault();
      stop();
      applyInput();
      draw();
    }, eventOptions);
    controls.prev.addEventListener("click", () => jump(index - 1), eventOptions);
    controls.next.addEventListener("click", () => jump(index + 1), eventOptions);
    progress.addEventListener("input", () => jump(Number(progress.value)), eventOptions);
    controls.play.addEventListener("click", () => {
      if (timer !== undefined) {
        stop();
      } else {
        if (index === frames.length - 1) index = 0;
        timer = window.setInterval(() => {
          if (!host.isConnected) {
            stop();
            return;
          }
          index += 1;
          draw();
        }, 1150);
      }
      draw();
    }, eventOptions);

    applyInput();
    draw();
    return {
      key,
      pause() {
        if (timer !== undefined) {
          stop();
          draw();
        }
      },
      dispose() {
        stop();
        events.abort();
        root.replaceChildren();
      }
    };
  }

  function pageTheme() {
    const styleScheme = document.body?.getAttribute("data-md-color-scheme")
      || document.documentElement.getAttribute("data-md-color-scheme");
    if (styleScheme === "slate" || styleScheme === "dark") return "dark";
    if (styleScheme === "default" || styleScheme === "light") return "light";
    const theme = document.body?.getAttribute("data-theme") || document.documentElement.getAttribute("data-theme");
    return theme === "dark" || theme === "light" ? theme : null;
  }

  function sync() {
    for (const [host, instance] of instances) {
      if (host.isConnected && host.matches(selector) && host.dataset.algorithm === instance.key) continue;
      instance.dispose();
      instances.delete(host);
    }
    const theme = pageTheme();
    for (const host of document.querySelectorAll(selector)) {
      const key = host.dataset.algorithm;
      if (!Object.hasOwn(algorithms, key)) continue;
      if (theme) {
        if (host.getAttribute("data-demo-theme") !== theme) host.setAttribute("data-demo-theme", theme);
      } else if (host.hasAttribute("data-demo-theme")) {
        host.removeAttribute("data-demo-theme");
      }
      if (!instances.has(host)) instances.set(host, mount(host, key));
    }
  }

  // Material instant navigation replaces the document content without reloading the script.
  window[bootKey] = sync;
  const observer = new MutationObserver(sync);
  observer.observe(document.documentElement, {
    subtree: true,
    childList: true,
    attributes: true,
    attributeFilter: ["data-algorithm", "data-md-color-scheme", "data-theme"]
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) for (const instance of instances.values()) instance.pause();
  });
  sync();
})();
