# Copyright 2017 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class LiquidityConstraintMixin(object):
    """
    Mixin class providing reduction of backtest weights based on available
    liquidity.
    """
    LIQUDITY_VOLUME_WINDOW = 15 # Window for computing median volume
    MAX_PERIOD_VOLUME_PCT = None

    def get_max_allowed_quantities(self, prices):
        """
        Returns the allowed quantity based on available liquidity, reducing
        quantity by MAX_PERIOD_VOLUME_PCT.
        """
        max_allowed_quantities = super(LiquidityConstraintMixin, self).get_max_allowed_quantities(prices)

        if not self.LIQUDITY_VOLUME_WINDOW or not self.MAX_PERIOD_VOLUME_PCT:
            return max_allowed_quantities

        volumes = prices.loc["Volume"].fillna(0)
        median_volumes = volumes.rolling(self.LIQUDITY_VOLUME_WINDOW).median()
        # Compute median volume (Shift to make sure we're not using the volume
        # of an incomplete day)
        volume_allowed_quantities = (median_volumes.shift() * self.MAX_PERIOD_VOLUME_PCT).round()

        if max_allowed_quantities is None:
            return volume_allowed_quantities

        max_allowed_quantities = volume_allowed_quantities.where(volume_allowed_quantities < max_allowed_quantities, max_allowed_quantities)

        return max_allowed_quantities
