<script>
  import * as d3 from 'd3';

  let { data = [], onFileSelect } = $props();

  let svgElement = $state(null);

  $effect(() => {
    if (data.length > 0 && svgElement) {
      renderTreeMap();
    }
  });

  function renderTreeMap() {
    const container = svgElement.parentElement;
    const width = container?.clientWidth || 800;
    const height = container?.clientHeight || 500;

    const svg = d3.select(svgElement)
      .attr("viewBox", [0, 0, width, height]);

    svg.selectAll("*").remove();

    const defs = svg.append("defs");
    const filter = defs.append("filter").attr("id", "glow");
    filter.append("feGaussianBlur").attr("stdDeviation", "2").attr("result", "blur");
    const merge = filter.append("feMerge");
    merge.append("feMergeNode").attr("in", "blur");
    merge.append("feMergeNode").attr("in", "SourceGraphic");

    const root = d3.hierarchy({
      name: "root",
      children: buildHierarchy(data)
    })
    .sum(d => d.size_bytes || 100)
    .sort((a, b) => b.value - a.value);

    d3.treemap()
      .size([width, height])
      .padding(3)
      .round(true)
      (root);

    const colorScale = {
      'safe':       { fill: '#1a3a2a', stroke: '#3fb950', text: '#3fb950' },
      'caution':    { fill: '#2d2a1a', stroke: '#d29922', text: '#d29922' },
      'restricted': { fill: '#2d1a1a', stroke: '#f85149', text: '#f85149' },
    };
    const defaultColor = { fill: '#21262d', stroke: '#30363d', text: '#8b949e' };

    const leaves = root.leaves();

    const nodes = svg.selectAll("g")
      .data(leaves)
      .join("g")
      .attr("transform", d => `translate(${d.x0},${d.y0})`);

    nodes.append("rect")
      .attr("width", d => Math.max(0, d.x1 - d.x0))
      .attr("height", d => Math.max(0, d.y1 - d.y0))
      .attr("rx", 4)
      .attr("fill", d => (colorScale[d.data.zone] || defaultColor).fill)
      .attr("stroke", d => (colorScale[d.data.zone] || defaultColor).stroke)
      .attr("stroke-width", 1.5)
      .attr("cursor", d => d.data.path ? "pointer" : "default")
      .style("transition", "filter 0.2s, stroke-width 0.2s")
      .on("mouseenter", function(event, d) {
        d3.select(this).attr("stroke-width", 2.5).style("filter", "url(#glow)");
        tooltip
          .style("opacity", 1)
          .html(`<strong>${d.data.name}</strong>${d.data.zone ? `<br/><span style="color:${(colorScale[d.data.zone] || defaultColor).text}">${d.data.zone}</span>` : ''}`);
      })
      .on("mousemove", function(event) {
        tooltip
          .style("left", (event.offsetX + 12) + "px")
          .style("top", (event.offsetY - 10) + "px");
      })
      .on("mouseleave", function() {
        d3.select(this).attr("stroke-width", 1.5).style("filter", "none");
        tooltip.style("opacity", 0);
      })
      .on("click", (event, d) => {
        if (d.data.path) onFileSelect(d.data);
      });

    nodes.append("text")
      .attr("x", 6)
      .attr("y", 16)
      .attr("font-size", "11px")
      .attr("font-family", "'Inter', sans-serif")
      .attr("font-weight", "500")
      .attr("fill", d => (colorScale[d.data.zone] || defaultColor).text)
      .attr("pointer-events", "none")
      .text(d => {
        const w = d.x1 - d.x0;
        const name = d.data.name || d.data.filename || '';
        if (w < 45) return '';
        if (w < 80) return name.length > 8 ? name.slice(0, 7) + '…' : name;
        return name;
      });

    const tooltip = d3.select(svgElement.parentElement)
      .selectAll(".treemap-tooltip")
      .data([0])
      .join("div")
      .attr("class", "treemap-tooltip")
      .style("position", "absolute")
      .style("opacity", 0)
      .style("background", "#1c2128")
      .style("border", "1px solid #30363d")
      .style("border-radius", "6px")
      .style("padding", "6px 10px")
      .style("font-size", "12px")
      .style("color", "#e1e4e8")
      .style("pointer-events", "none")
      .style("z-index", "10")
      .style("box-shadow", "0 4px 12px rgba(0,0,0,0.4)");
  }

  function buildHierarchy(files) {
    const root = { name: 'root', children: [] };

    files.forEach(file => {
      const pathParts = file.path.split('/');
      let current = root;

      pathParts.forEach((part, index) => {
        let child = current.children.find(c => c.name === part);
        if (!child) {
          child = { name: part, children: [] };
          current.children.push(child);
        }
        current = child;

        if (index === pathParts.length - 1) {
          // It's the file itself
          // We add the file data to this node
          Object.assign(current, file);
          // Remove its children since it's a leaf
          current.children = [];
        }
      });
    });
    return root.children;
  }
</script>

<div class="treemap-container">
  {#if data.length === 0}
    <div class="placeholder">No data loaded. Enter a URL to begin.</div>
  {:else}
    <svg bind:this={svgElement}></svg>
  {/if}
</div>

<style>
  .treemap-container {
    width: 100%;
    height: 100%;
    background: #0d1117;
    overflow: hidden;
    position: relative;
  }
  .placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #484f58;
    font-style: italic;
    font-size: 0.9rem;
  }
  svg {
    display: block;
    width: 100%;
    height: 100%;
  }
</style>
