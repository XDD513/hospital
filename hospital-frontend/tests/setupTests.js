import { config } from '@vue/test-utils'

config.global.stubs = {
  'el-empty': {
    template: `
      <div class="el-empty">
        <div class="slot-description">
          <slot name="description"></slot>
        </div>
        <div class="slot-default">
          <slot></slot>
        </div>
        <div class="slot-bottom">
          <slot name="bottom"></slot>
        </div>
      </div>
    `
  }
}


