import { mount } from '@vue/test-utils'
import EmptyState from '@/components/common/EmptyState.vue'

describe('EmptyState.vue', () => {
  it('renders description and tip props', () => {
    const wrapper = mount(EmptyState, {
      props: {
        description: '暂无数据',
        tip: '请稍后重试'
      }
    })

    expect(wrapper.find('.empty-description p').text()).toBe('暂无数据')
    expect(wrapper.find('.empty-description small').text()).toBe('请稍后重试')
  })

  it('renders default and bottom slots', () => {
    const wrapper = mount(EmptyState, {
      slots: {
        default: '<button class="retry-btn">重试</button>',
        bottom: '<div class="extra">其他内容</div>'
      }
    })

    expect(wrapper.find('.retry-btn').exists()).toBe(true)
    expect(wrapper.find('.extra').exists()).toBe(true)
  })
})


