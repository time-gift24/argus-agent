<template>
  <PageBodyShell
    :breadcrumbs="['仪表盘']"
    :description="`监控分布式智能体架构中的高频决策循环，当前追踪 ${agentStore.agents.length} 个并发流。`"
    title="智能体总览"
  >
    <div class="grid grid-cols-12 gap-6">

      <!-- Hero Process Map -->
      <div class="col-span-12 lg:col-span-8 bg-surface-container-lowest rounded-[2rem] p-8 overflow-hidden relative shadow-sm border border-outline-variant/30 animate-fade-up animate-delay-1">
        <div class="flex justify-between items-start mb-12">
          <div>
            <span class="text-[10px] font-bold tracking-[0.2em] text-primary uppercase block mb-1">实时工作流</span>
            <h2 class="text-2xl font-headline font-bold">神经网络分布图</h2>
          </div>
          <div class="flex gap-2">
            <span class="flex items-center gap-1.5 px-3 py-1 bg-tertiary-fixed text-on-tertiary-fixed rounded-full text-xs font-bold">
              <span class="w-2 h-2 rounded-full bg-tertiary-fixed-dim glow-pulse"></span>
              稳定
            </span>
          </div>
        </div>

        <!-- Process Map -->
        <div class="relative h-64 flex items-center justify-center">
          <div class="absolute inset-0 flex items-center justify-around px-12">
            <!-- Node 1: INPUT -->
            <div class="z-10 bg-white shadow-xl p-4 rounded-2xl flex flex-col items-center gap-2 transition-transform hover:scale-105">
              <div class="w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center text-primary">
                <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
                </svg>
              </div>
              <span class="text-[10px] font-bold text-on-surface-variant">输入</span>
            </div>

            <!-- Flow Line 1 -->
            <div class="h-[2px] flex-grow bg-gradient-to-r from-primary-fixed-dim via-primary to-primary-container relative">
              <div class="absolute -top-1 left-1/2 w-2 h-2 rounded-full bg-white border-2 border-primary"></div>
            </div>

            <!-- Node 2: Azure Core (Glassmorphic) -->
            <div class="z-10 glass-panel shadow-2xl p-6 rounded-[2rem] flex flex-col items-center gap-3 ring-1 ring-primary/10 scale-110">
              <div class="w-16 h-16 rounded-full bg-gradient-to-tr from-primary to-primary-container flex items-center justify-center text-white shadow-lg">
                <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2a8 8 0 0 1 8 8v4a8 8 0 0 1-16 0v-4a8 8 0 0 1 8-8z"/>
                  <path d="M9 12h.01M15 12h.01"/>
                </svg>
              </div>
              <div class="text-center">
                <span class="text-xs font-bold text-primary uppercase tracking-tighter">Azure Core</span>
                <p class="text-[10px] text-on-surface-variant">处理中...</p>
              </div>
            </div>

            <!-- Flow Line 2 -->
            <div class="h-[2px] flex-grow bg-gradient-to-r from-primary-container via-primary-fixed-dim to-slate-200"></div>

            <!-- Node 3: OUTPUT -->
            <div class="z-10 bg-white shadow-xl p-4 rounded-2xl flex flex-col items-center gap-2 transition-transform hover:scale-105 opacity-60">
              <div class="w-12 h-12 rounded-full bg-surface-container flex items-center justify-center text-on-surface-variant">
                <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/>
                  <path d="M12 12v9"/>
                  <path d="m8 17 4 4 4-4"/>
                </svg>
              </div>
              <span class="text-[10px] font-bold text-on-surface-variant">输出</span>
            </div>
          </div>

          <!-- Decorative Background Waves -->
          <svg class="absolute inset-0 w-full h-full opacity-10" viewBox="0 0 800 200">
            <path d="M0,100 C150,50 350,150 500,100 C650,50 800,100 800,100" fill="none" stroke="#003ec7" stroke-width="2"/>
            <path d="M0,120 C150,70 350,170 500,120 C650,70 800,120 800,120" fill="none" stroke="#0052ff" stroke-width="1"/>
          </svg>
        </div>
      </div>

      <!-- Performance Analytics (Right Column) -->
      <div class="col-span-12 lg:col-span-4 space-y-6 animate-fade-up animate-delay-2">
        <!-- Throughput Chart -->
        <div class="bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30">
          <h3 class="font-headline font-bold text-lg mb-6 flex justify-between items-center">
            吞吐量
            <svg class="w-4 h-4 text-on-surface-variant" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>
            </svg>
          </h3>
          <div class="flex items-end gap-2 h-32 mb-4 px-2">
            <div v-for="(bar, i) in throughputBars" :key="i"
              class="w-full rounded-t-lg transition-all duration-300 hover:opacity-80"
              :class="bar.color"
              :style="{ height: bar.height + '%' }"
            ></div>
          </div>
          <div class="flex justify-between text-[10px] font-bold text-on-surface-variant uppercase tracking-widest px-1">
            <span>08:00</span>
            <span>12:00</span>
            <span>16:00</span>
          </div>
        </div>

        <!-- System Health Card -->
        <div class="bg-primary text-on-primary rounded-[2rem] p-6 shadow-lg relative overflow-hidden">
          <div class="relative z-10">
            <p class="text-[10px] font-bold tracking-widest uppercase opacity-70 mb-1">系统健康</p>
            <h4 class="text-3xl font-headline font-bold">99.98%</h4>
            <div class="mt-4 flex items-center gap-2">
              <span class="text-xs bg-white/20 px-2 py-0.5 rounded-full">已优化</span>
            </div>
          </div>
          <div class="absolute -right-8 -bottom-8 w-32 h-32 bg-primary-container rounded-full blur-3xl opacity-50"></div>
        </div>
      </div>

      <!-- Agent Registry Section -->
      <div class="col-span-12 animate-fade-up animate-delay-3">
        <div class="flex justify-between items-end mb-6">
          <div>
            <h2 class="text-3xl font-headline font-bold tracking-tight">智能体注册表</h2>
            <p class="text-on-surface-variant text-sm">已部署智能体节点的实时状态。</p>
          </div>
          <div class="flex gap-4">
            <tiny-button plain>
              <span class="text-xs font-bold">筛选: 全部</span>
            </tiny-button>
            <tiny-button plain>
              <span class="text-xs font-bold">排序: 性能</span>
            </tiny-button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <!-- Agent Card: Active -->
          <div
            v-for="agent in agents"
            :key="agent.id"
            class="bg-surface-container-lowest p-6 rounded-[2rem] shadow-sm relative group hover:shadow-xl transition-all duration-300 border border-outline-variant/30"
          >
            <!-- Status Badge -->
            <div class="absolute top-6 right-6">
              <span class="flex items-center gap-1 text-[10px] font-bold" :class="agent.statusClass">
                <span class="w-2 h-2 rounded-full" :class="[agent.dotClass, agent.status === 'Active' ? 'glow-pulse' : '']"></span>
                {{ agent.status.toUpperCase() }}
              </span>
            </div>

            <!-- Agent Info -->
            <div class="flex items-start gap-4 mb-6">
              <div class="w-14 h-14 rounded-2xl overflow-hidden shadow-inner bg-surface-container flex items-center justify-center text-primary text-2xl font-headline font-bold">
                {{ agent.avatar }}
              </div>
              <div>
                <h4 class="font-headline font-bold text-lg leading-tight">{{ agent.name }}</h4>
                <p class="text-xs text-on-surface-variant font-medium">{{ agent.role }}</p>
              </div>
            </div>

            <!-- Metric -->
            <div class="space-y-3 mb-6">
              <div class="flex justify-between text-xs">
                <span class="text-on-surface-variant">{{ agent.metricLabel }}</span>
                <span class="font-bold">{{ agent.metricValue }}</span>
              </div>
              <div class="w-full h-1.5 bg-surface-container rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  :class="agent.barColor"
                  :style="{ width: agent.metricPercent + '%' }"
                ></div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2">
              <button class="flex-grow py-2 rounded-xl text-xs font-bold transition-colors cursor-pointer"
                :class="agent.status === 'Idle' ? 'bg-primary text-on-primary hover:bg-primary-container' : 'bg-surface-container text-on-surface hover:bg-surface-container-high'"
              >
                {{ agent.primaryAction }}
              </button>
              <button class="px-3 py-2 rounded-xl bg-surface-container text-on-surface-variant hover:text-primary transition-colors cursor-pointer">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Elite Card: Vanguard-Alpha -->
          <div class="bg-surface-container-lowest p-6 rounded-[2rem] shadow-sm relative overflow-hidden group hover:shadow-xl transition-all duration-300 border border-outline-variant/30">
            <div class="absolute top-0 right-0 w-24 h-24 bg-primary/5 rounded-bl-[4rem]"></div>
            <div class="absolute top-6 right-6">
              <span class="flex items-center gap-1 text-[10px] font-bold text-primary">
                <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2L9 9l-7 1 5 5-1.5 7L12 18.5 18.5 22 17 15l5-5-7-1z"/>
                </svg>
                ELITE
              </span>
            </div>
            <div class="flex items-start gap-4 mb-6">
              <div class="w-14 h-14 rounded-2xl overflow-hidden shadow-inner bg-surface-container flex items-center justify-center text-primary text-2xl font-headline font-bold">
                V
              </div>
              <div>
                <h4 class="font-headline font-bold text-lg leading-tight">Vanguard-Alpha</h4>
                <p class="text-xs text-on-surface-variant font-medium">安全与漏洞防御</p>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="bg-surface-container p-3 rounded-2xl">
                <p class="text-[10px] text-on-surface-variant font-bold uppercase mb-1">成功率</p>
                <p class="text-xl font-headline font-bold text-primary">100%</p>
              </div>
              <div class="bg-surface-container p-3 rounded-2xl">
                <p class="text-[10px] text-on-surface-variant font-bold uppercase mb-1">延迟</p>
                <p class="text-xl font-headline font-bold text-primary">8ms</p>
              </div>
            </div>
            <button class="w-full py-2.5 rounded-xl border border-primary/20 text-primary text-xs font-bold hover:bg-primary/5 transition-colors cursor-pointer">
              完整分析
            </button>
          </div>
        </div>
      </div>

      <!-- Execution Loops Table -->
      <div class="col-span-12 bg-surface-container-lowest rounded-[2rem] p-8 shadow-sm border border-outline-variant/30 animate-fade-up animate-delay-4">
        <div class="flex justify-between items-center mb-8">
          <h3 class="font-headline text-2xl font-bold">最近执行循环</h3>
          <tiny-button type="text">
            <span class="text-sm text-primary font-bold flex items-center gap-1">
              查看完整日志
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </span>
          </tiny-button>
        </div>

        <div class="overflow-x-auto">
          <tiny-grid :data="executions" border resizable auto-resize>
            <tiny-grid-column field="id" title="ID" width="100">
              <template #default="{ row }">
                <span class="text-xs font-mono text-on-surface-variant">{{ row.id }}</span>
              </template>
            </tiny-grid-column>

            <tiny-grid-column field="processName" title="流程名称">
              <template #default="{ row }">
                <span class="text-sm font-bold">{{ row.processName }}</span>
              </template>
            </tiny-grid-column>

            <tiny-grid-column field="initiator" title="发起者" width="140">
              <template #default="{ row }">
                <div class="flex items-center gap-2">
                  <div class="w-6 h-6 rounded-full" :class="row.initiatorBg"></div>
                  <span class="text-xs">{{ row.initiator }}</span>
                </div>
              </template>
            </tiny-grid-column>

            <tiny-grid-column field="runtime" title="运行时间" width="100">
              <template #default="{ row }">
                <span class="text-xs">{{ row.runtime }}</span>
              </template>
            </tiny-grid-column>

            <tiny-grid-column field="confidence" title="置信度" width="140">
              <template #default="{ row }">
                <div class="flex items-center gap-2">
                  <div class="w-16 h-1 bg-surface-container rounded-full overflow-hidden">
                    <div class="bg-primary h-full" :style="{ width: row.confidence + '%' }"></div>
                  </div>
                  <span class="text-[10px] font-bold text-primary">{{ row.confidence }}%</span>
                </div>
              </template>
            </tiny-grid-column>

            <tiny-grid-column field="result" title="结果" width="100">
              <template #default="{ row }">
                <span class="px-2 py-0.5 bg-tertiary-fixed text-on-tertiary-fixed rounded text-[10px] font-bold uppercase">{{ row.result }}</span>
              </template>
            </tiny-grid-column>
          </tiny-grid>
        </div>
      </div>

    </div>
  </PageBodyShell>
</template>

<script setup>
import { Grid as TinyGrid, GridColumn as TinyGridColumn, Button as TinyButton } from '@opentiny/vue'
import PageBodyShell from '../components/PageBodyShell.vue'
import { useAgentStore } from '../stores/agents'

const agentStore = useAgentStore()

const throughputBars = [
  { height: 40, color: 'bg-primary-fixed-dim' },
  { height: 65, color: 'bg-primary' },
  { height: 50, color: 'bg-primary-container' },
  { height: 85, color: 'bg-primary' },
  { height: 60, color: 'bg-primary-fixed-dim' },
  { height: 45, color: 'bg-primary' },
  { height: 75, color: 'bg-primary-container' },
]

const agents = [
  {
    id: 1,
    name: 'Lumina-4',
    avatar: 'L4',
    role: '市场情绪分析师',
    status: 'Active',
    statusClass: 'text-tertiary-fixed-dim',
    dotClass: 'bg-tertiary-fixed-dim',
    metricLabel: '认知负载',
    metricValue: '42%',
    metricPercent: 42,
    barColor: 'bg-primary',
    primaryAction: '配置',
  },
  {
    id: 2,
    name: 'Nexus-7',
    avatar: 'N7',
    role: '数据管道编排器',
    status: 'Idle',
    statusClass: 'text-on-surface-variant',
    dotClass: 'bg-slate-300',
    metricLabel: '运行时间',
    metricValue: '14d 2h',
    metricPercent: 100,
    barColor: 'bg-slate-300',
    primaryAction: '唤醒智能体',
  },
]

const executions = [
  {
    id: '#AX-2094',
    processName: '市场再平衡循环',
    initiator: 'Lumina-4',
    initiatorBg: 'bg-primary-fixed',
    runtime: '142ms',
    confidence: 98,
    result: 'Success',
  },
  {
    id: '#AX-2093',
    processName: '跨链审计',
    initiator: 'Nexus-7',
    initiatorBg: 'bg-slate-200',
    runtime: '1,204ms',
    confidence: 82,
    result: 'Success',
  },
  {
    id: '#AX-2092',
    processName: '威胁向量分析',
    initiator: 'Vanguard-Alpha',
    initiatorBg: 'bg-primary-fixed',
    runtime: '67ms',
    confidence: 100,
    result: 'Success',
  },
  {
    id: '#AX-2091',
    processName: '情绪聚合',
    initiator: 'Lumina-4',
    initiatorBg: 'bg-primary-fixed',
    runtime: '234ms',
    confidence: 91,
    result: 'Success',
  },
]
</script>
