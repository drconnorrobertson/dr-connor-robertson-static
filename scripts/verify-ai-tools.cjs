const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.join(__dirname,'../dist/ai/implementation');
function script(file,marker){const html=fs.readFileSync(path.join(root,file,'index.html'),'utf8');return [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes(marker));}
function element(){return {textContent:'',value:'',hidden:false,children:[],events:{},addEventListener(event,fn){this.events[event]=fn;},append(child){this.children.push(child);},replaceChildren(...children){this.children=children;}};}
const form=element(),query=element(),category=element(),count=element(),empty=element();
const cards=[['Invoice review','Finance'],['Vendor contract review','Finance'],['Interview content','Content']].map(([text,group])=>Object.assign(element(),{textContent:text,dataset:{category:group}}));
const ids={'directory-form':form,'directory-query':query,'directory-category':category,'directory-count':count,'directory-empty':empty};
vm.runInNewContext(script('directory','directory-form'),{document:{getElementById:id=>ids[id],querySelectorAll:()=>cards}});
query.value='invoice review';query.events.input();assert.equal(count.textContent,'1 of 3 guides');assert.equal(cards[0].hidden,false);assert.equal(cards[1].hidden,true);
category.value='Content';category.events.change();assert.equal(empty.hidden,false);assert.equal(count.textContent,'0 of 3 guides');
form.events.reset();assert.equal(count.textContent,'3 of 3 guides');assert.equal(query.value,'');assert.equal(category.value,'');
const planner=element(),result=element();let checked=new Set();
vm.runInNewContext(script('readiness-planner','readiness-form'),{document:{getElementById:id=>id==='readiness-form'?planner:result,createElement:()=>element()},FormData:class{has(key){return checked.has(key);}}});
planner.events.submit({preventDefault(){}});assert.equal(result.children[0].textContent,'0 of 6 prerequisites documented');assert.equal(result.children[2].children.length,6);
checked=new Set(['owner','sources']);planner.events.submit({preventDefault(){}});assert.equal(result.children[2].children.length,4);assert.match(result.children[2].children[0].textContent,/Measure preparation/);
checked=new Set(['owner','sources','baseline','tests','recovery','capacity']);planner.events.submit({preventDefault(){}});assert.equal(result.children[0].textContent,'6 of 6 prerequisites documented');assert.equal(result.children[2].children.length,0);assert.match(result.children[1].textContent,/bounded pilot/);
console.log('PASS: directory multiword search, category intersection, empty state, reset; readiness none, partial, and all prerequisites');
